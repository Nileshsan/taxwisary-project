from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def regime_advisory(request):
    context = {}
    return render(request, "regime/regime.html", context)


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def regime_ai(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            extracted = data.get("extracted_data", {})
            salary = float(extracted.get("salary", 0))
            hra = float(extracted.get("hra", 0))
            deductions = float(extracted.get("deductions", 0))

            # Example regime advice logic
            if deductions > 150000:
                advice = "Old Regime may be better due to high deductions."
            elif salary < 700000:
                advice = "New Regime may be better for lower salary."
            else:
                advice = "Please consult a tax expert for best advice."

            return HttpResponse(advice)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)









