import re
from io import BytesIO
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


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


# utils.py
import requests

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
