import re
from io import BytesIO
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import requests


def chatbot_view(request):
    """
    Django view to handle chatbot queries and return structured extracted data.
    """
    user_input = request.GET.get("query", "").strip()

    if not user_input:
        return JsonResponse({"error": "No input provided"}, status=400)

    extracted_info = extract_data(user_input)

    return JsonResponse({"response": extracted_info})

def generate_pdf(data):
    """
    Generates a PDF from extracted data and returns it as an HTTP response.
    """

    # Ensure data is valid
    if not data:
        return HttpResponse("No data provided for PDF generation.", status=400)

    try:
        # Load template and render with data
        template = get_template('users/pdf_template.html')

        html_content = template.render({'data': data})

        # Convert HTML to PDF
        pdf_result = BytesIO()
        pdf = pisa.CreatePDF(html_content, dest=pdf_result)

        if pdf.err:
            return HttpResponse("Failed to generate PDF.", status=500)

        # Prepare response with PDF
        response = HttpResponse(pdf_result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="tax_report.pdf"'
        return response

    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


def extract_from_doc(file):
    # Placeholder parsing logic
    return {
        "salary": 900000,
        "deductions": 150000,
        "hra": 100000,
        "pan": "ABCDE1234F"
    }

def calculate_and_prompt_ai(data):
    salary = float(data.get("salary", 0))
    deductions = float(data.get("deductions", 0))

    old_tax = calculate_tax_old(salary - deductions)
    new_tax = calculate_tax_new(salary)

    regime = "Old Regime" if old_tax < new_tax else "New Regime"

    prompt = f"""
    Salary: ₹{salary}
    Deductions: ₹{deductions}

    Based on the Indian tax regime rules, recommend the better regime and explain why.
    """

    # Call your local Mistral/LLaMA API (replace localhost with server IP if needed)
    res = requests.post("http://localhost:5000/query", json={"prompt": prompt})
    return res.json().get("response", f"{regime} is better. Tax Old: ₹{old_tax}, New: ₹{new_tax}")

def calculate_tax_old(income):
    if income <= 250000:
        return 0
    elif income <= 500000:
        return (income - 250000) * 0.05
    elif income <= 1000000:
        return 12500 + (income - 500000) * 0.2
    else:
        return 112500 + (income - 1000000) * 0.3

def calculate_tax_new(income):
    if income <= 300000:
        return 0
    elif income <= 600000:
        return (income - 300000) * 0.05
    elif income <= 900000:
        return 15000 + (income - 600000) * 0.1
    else:
        return 45000 + (income - 900000) * 0.15

def regime_advice_logic(salary, hra, deductions):
    """
    Returns a dict with detailed regime comparison and recommendation.
    salary: total gross salary (float)
    hra: HRA exemption (float)
    deductions: total deductions (float)
    """
    # Old Regime
    taxable_old = max(salary - hra - deductions, 0)
    old_tax = calculate_tax_old(taxable_old)
    # New Regime (no deductions, no HRA)
    taxable_new = max(salary, 0)
    new_tax = calculate_tax_new(taxable_new)
    # Suggestion
    if old_tax < new_tax:
        suggestion = "Old Tax Regime"
        recommended = {"taxable_income": taxable_old, "tax": old_tax}
    elif new_tax < old_tax:
        suggestion = "New Tax Regime"
        recommended = {"taxable_income": taxable_new, "tax": new_tax}
    else:
        suggestion = "Either Regime"
        recommended = {"taxable_income": taxable_new, "tax": new_tax}
    # Excess deduction needed for break even
    tax_diff = abs(old_tax - new_tax)
    if taxable_old > 1000000:
        excess = tax_diff / 0.3 if tax_diff else 0
    elif taxable_old > 500000:
        excess = tax_diff / 0.2 if tax_diff else 0
    else:
        excess = 0
    return {
        "suggestion": suggestion,
        "recommended": recommended,
        "old_regime": {"taxable_income": taxable_old, "tax": old_tax},
        "new_regime": {"taxable_income": taxable_new, "tax": new_tax},
        "excess_deduction": round(excess, 2)
    }
