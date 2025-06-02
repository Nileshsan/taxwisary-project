from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import re
import PyPDF2


def regime_advisory(request):
    return render(request, "regime/regime.html", {})

# --- Tax Calculation Logic ---

def calculate_old_regime_tax(salary, hra, deductions):
    taxable_income = max(salary - 50000 - hra - deductions, 0)
    if taxable_income <= 250000:
        tax = 0
    elif taxable_income <= 500000:
        tax = (taxable_income - 250000) * 0.05
    elif taxable_income <= 1000000:
        tax = 12500 + (taxable_income - 500000) * 0.2
    else:
        tax = 112500 + (taxable_income - 1000000) * 0.3
    # For taxable_income <= 500000, force tax to be zero
    if taxable_income <= 500000:
        tax = 0
    tax = tax * 1.04  # add 4% cess
    return round(tax, 2), taxable_income

def calculate_new_regime_tax(salary):
    taxable_income = (salary - 75000)  # standard deduction
    if taxable_income <= 300000:
        tax = 0
    elif taxable_income <= 700000:
        tax = (taxable_income - 300000) * 0.05
    elif taxable_income <= 1000000:
        tax = 20000 + (taxable_income - 700000) * 0.1
    elif taxable_income <= 1200000:
        tax = 50000 + (taxable_income - 1000000) * 0.15
    elif taxable_income <= 1500000:
        tax = 80000 + (taxable_income - 1200000) * 0.2
    else:
        tax = 140000 + (taxable_income - 1500000) * 0.3
    if taxable_income <= 700000:
        tax = 0
    tax = tax * 1.04  # add 4% cess
    return round(tax, 2), taxable_income


def calculate_excess_tax(old_tax, new_tax, taxable_income):
    """
    Calculates an extra tax component based on the difference between old and new
    regime tax calculations and the taxable income (after exemptions/deductions).

    Conversion: taxable_income (in rupees) is converted to lakhs:
      if taxable income is between 5-10 lakhs, excess tax = difference * 20%
      if above 10 lakhs, excess tax = difference * 30%
      otherwise, excess tax is 0.
    """
    tax_diff = abs(old_tax - new_tax)
    taxable_in_lakhs = taxable_income / 100000.0
    if 5 <= taxable_in_lakhs <= 10:
        excess = tax_diff / 0.20
    elif taxable_in_lakhs > 10:
        excess = tax_diff / 0.30
    else:
        excess = 0
    return round(excess, 2)

def regime_advice_logic(salary, hra, deductions):
    old_tax, old_taxable_income = calculate_old_regime_tax(salary, hra, deductions)
    new_tax, new_taxable_income = calculate_new_regime_tax(salary)
    
    excess_deducations = calculate_excess_tax(old_tax, new_tax, old_taxable_income)
    
    if old_tax < new_tax:
        suggestion = "✅ Old Regime may be better."
        selected = {
            "taxable_income": old_taxable_income,
            "tax": old_tax
        }
    elif new_tax < old_tax:
        suggestion = "✅ New Regime may be better."
        selected = {
            "taxable_income": new_taxable_income,
            "tax": new_tax
        }
    else:
        suggestion = "Both regimes result in the same tax. Choose based on convenience."
        selected = {
            "taxable_income": new_taxable_income,
            "tax": new_tax
        }
    
    return {
        "suggestion": suggestion,
        "selected_regime": selected,
        "old_regime": {
            "taxable_income": old_taxable_income,
            "tax": old_tax
        },
        "new_regime": {
            "taxable_income": new_taxable_income,
            "tax": new_tax
        },
        "excess_Deducation": excess_deducations  # extra tax component based on the difference criteria
    }




def safe_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import re
import PyPDF2

@csrf_exempt
def regime_ai(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Debug output
            extracted = data.get("extracted_data", data)
            salary = safe_float(extracted.get("salary", 0))
            hra = safe_float(extracted.get("hra", 0))
            deductions = safe_float(extracted.get("deductions", extracted.get("investment", 0)))
            if salary <= 0:
                return JsonResponse({
                    "status": "error",
                    "error": "Salary must be greater than 0."
                }, status=400)
            result = regime_advice_logic(salary, hra, deductions)
            result["status"] = "success"
            print("Returning from regime_ai:", result)  # Debug output
            return JsonResponse(result)
        except Exception as e:
            import traceback
            print("Error in regime_ai:", traceback.format_exc())
            return JsonResponse({
                "status": "error",
                "error": f"Invalid input or server error: {str(e)}"
            }, status=400)
    return JsonResponse({"status": "error", "error": "Invalid request method."}, status=400)





import os
import re
import json
import PyPDF2
import pytesseract
from PIL import Image
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import tempfile

def parse_image(file_path):
    extracted = {}
    try:
        img = Image.open(file_path)
        # Preprocessing: convert image to grayscale
        img = img.convert("L")
        # Apply binary thresholding – adjust threshold value as needed
        img = img.point(lambda x: 0 if x < 140 else 255, "1")
        # Set custom Tesseract config (OEM and PSM)
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(img, config=custom_config)
        
        # Now use the same regex to extract values
        salary_match = re.search(r"Annual Salary[:\s]+([\d,]+)", text, re.IGNORECASE)
        hra_match = re.search(r"HRA[:\s]+([\d,]+)", text, re.IGNORECASE)
        deductions_match = re.search(r"(80C Deductions|Investments \(80C\))[:\s]+([\d,]+)", text, re.IGNORECASE)
        if salary_match:
            extracted['salary'] = salary_match.group(1).replace(',', '')
        if hra_match:
            extracted['hra'] = hra_match.group(1).replace(',', '')
        if deductions_match:
            extracted['deductions'] = deductions_match.group(2).replace(',', '')
    except Exception as e:
        print("Error in parse_image:", e)
    return extracted 

def parse_document(file_path):
    extracted = {}
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        # Use the same regex to extract salary details
        salary_match = re.search(r"Annual Salary[:\s]+([\d,]+)", text, re.IGNORECASE)
        hra_match = re.search(r"HRA[:\s]+([\d,]+)", text, re.IGNORECASE)
        deductions_match = re.search(r"(80C Deductions|Investments \(80C\))[:\s]+([\d,]+)", text, re.IGNORECASE)
        if salary_match:
            extracted['salary'] = salary_match.group(1).replace(',', '')
        if hra_match:
            extracted['hra'] = hra_match.group(1).replace(',', '')
        if deductions_match:
            extracted['deductions'] = deductions_match.group(2).replace(',', '')
    except Exception as e:
        print("Error in parse_document:", e)
    return extracted

import tempfile

@csrf_exempt
def upload_doc(request):
    if request.method == "POST":
        files = request.FILES.getlist('document')
        if not files:
            return JsonResponse({'error': 'No document uploaded.'}, status=400)
        extracted_data = {}
        temp_dir = tempfile.gettempdir()  # get system temporary directory
        for file in files:
            file_path = os.path.join(temp_dir, file.name)
            try:
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                # Determine which parser to use based on file extension.
                ext = os.path.splitext(file.name)[1].lower()
                if ext in ['.pdf']:
                    data = parse_document(file_path)
                elif ext in ['.png', '.jpg', '.jpeg']:
                    data = parse_image(file_path)
                else:
                    data = {}
                extracted_data.update(data)
            except Exception as e:
                import traceback
                print("Error in upload_doc:", traceback.format_exc())
                return JsonResponse({'error': f'File processing failed: {str(e)}'}, status=400)
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)
        return JsonResponse(extracted_data)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
