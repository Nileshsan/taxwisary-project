from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#  Personal Information Flow

@login_required
def advisory_personal(request):
    if request.method == "POST":
        request.session.setdefault("temp_data", {})
        request.session["temp_data"].update({
            "full_name": request.POST.get("full_name", "").strip(),
            "dob": request.POST.get("dob", "").strip(),
            "phone": request.POST.get("phone", "").strip(),
            "email": request.POST.get("email", "").strip(),
        })
        request.session.modified = True
        return redirect(reverse("users:advisory_personal_confirm"))
    return render(request, "advisory/advisory_personal.html")

@login_required
def advisory_personal_confirm(request):
    personal_data = request.session.get("temp_data", {})
    if request.method == "POST":
        # Personal info confirmed – move to Income section.
        return redirect(reverse("users:advisory_income"))
    return render(request, "advisory/advisory_personal_confirm.html", {"personal_data": personal_data})


# Income Details Flow

@login_required
def advisory_income(request):
    if request.method == "POST":
        request.session.setdefault("temp_data", {})
        request.session["temp_data"].update({
            "employer_name": request.POST.get("employer_name", "").strip(),
            "tan": request.POST.get("tan", "").strip().upper(),
            "salary_income": request.POST.get("salary_income", "").strip(),
            # … add other income fields as needed.
        })
        request.session.modified = True
        return redirect(reverse("users:advisory_income_confirm"))
    return render(request, "advisory/advisory_income.html")

@login_required
def advisory_income_confirm(request):
    income_data = request.session.get("temp_data", {})
    if request.method == "POST":
        return redirect(reverse("users:advisory_deductions"))
    return render(request, "advisory/advisory_income_confirm.html", {"income_data": income_data})

# Deductions Flow

@login_required
def advisory_deductions(request):
    # Placeholder implementation: update as needed
    return render(request, "advisory/advisory_deductions.html")

#  Final Summary & Report Generation Flow

from .report_views import generate_report  # Import your report view

@login_required
def advisory_summary(request):
    # Display final summary before report generation.
    temp_data = request.session.get("temp_data", {})
    if request.method == "POST":
        # Call the report generation view (could be an internal function)
        return generate_report(request, temp_data)
    return render(request, "advisory/advisory_summary.html", {"temp_data": temp_data})



