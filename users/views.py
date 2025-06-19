from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.timezone import now
from django.db import transaction
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


# External Libraries
from cloudinary.uploader import upload
from reportlab.pdfgen import canvas  # Ensure ReportLab is installed
from xhtml2pdf import pisa

# Models
from .models import (
    UserProfile, IncomeDetails, Deductions,
    CapitalGainAndOtherIncome, TaxReport,
    TempUserData, TaxData
)

from users.models import TempIncomeDetails, TempUserData, UserProfile, TaxReport



# Utilities
from .utils import generate_pdf
from .chatbot_fsm import ChatFSM
from users.utils import regime_advice_logic

# Other
import json
import os
import re
from io import BytesIO
import requests
from urllib.parse import urlparse




def upload_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        upload_result = upload(file)
        return JsonResponse({'url': upload_result['secure_url']})
    return JsonResponse({'error': 'No file uploaded'}, status=400)


def home(request):
    return render(request, 'users/home.html')  # Make sure 'users/home.html' exists


def register(request):
    next_url = request.GET.get("next", "")
    
    if request.method == 'POST':
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if not username:
            messages.error(request, "Username is required!")
            return redirect("users:register")

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("users:register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("users:register")

        # Create user and auto-login
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        login(request, user)
        messages.success(request, f"Account created successfully! Welcome, {username}!")
        return redirect(next_url if next_url else "home")
    
    return render(request, 'users/register.html', {'next': next_url})

def login_view(request):
    next_url = request.GET.get("next", "/")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect(next_url or "home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "users/login.html", {"next": next_url})



def logout_view(request):
    logout(request)
    return redirect('/')

def regime_advisory(request):
    # Render the template from users/templates/users/regime.html
    return render(request, "users/regime.html")

from django.contrib.auth.decorators import login_required

@login_required
def edit_profile(request):
    # For now, simply render a placeholder template.
    return render(request, "users/edit_profile.html")

@login_required
def change_password(request):
    # For now, simply render a placeholder template; later add password form / logic.
    return render(request, "users/change_password.html")

@login_required
def dashboard(request):
    user_profile = None
    profile_pic_url = "https://via.placeholder.com/100"  # Default Image

    if hasattr(request.user, 'profile'):  # Ensure profile exists
        user_profile = request.user.profile
        if user_profile.profile_pic:  # Check if profile_pic is not empty
            profile_pic_url = user_profile.profile_pic.url

    return render(request, 'users/dashboard.html', {
        'user': request.user,
        'user_name': request.user.username,
        'user_email': request.user.email,
        'profile_pic': profile_pic_url

    })
    documents = UserDocument.objects.filter(user=request.user)
    tax_data = TaxData.objects.filter(user=request.user)
    form = FileUploadForm()
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()
            return redirect('dashboard')
    return render(request, 'users/dashboard.html', {
        'documents': documents,
        'tax_data': tax_data,
        'form': form
    })

def home(request):
    return render(request, 'users/home.html')  # Correct path

def home(request):
    return render(request, 'index.html')


def index(request):
    return render(request, 'index.html')  # Ensure 'index.html' exists in your templates folder

def base_view(request):
    salary = hra = deductions = None
    regime_result = None
    if request.method == "POST":
        salary = request.POST.get("salary")
        hra = request.POST.get("hra")
        deductions = request.POST.get("deductions")
        try:
            salary = float(salary)
        except (TypeError, ValueError):
            salary = 0
        try:
            hra = float(hra)
        except (TypeError, ValueError):
            hra = 0
        try:
            deductions = float(deductions)
        except (TypeError, ValueError):
            deductions = 0
        regime_result = regime_advice_logic(salary, hra, deductions)
    context = {
        "salary": salary,
        "hra": hra,
        "deductions": deductions,
        "regime_result": regime_result,
    }
    return render(request, "users/base.html", context)


def users_home(request):
    return render(request, 'users/home.html')

def profile_view(request):
    return render(request, 'users/profile.html')

def main_page(request):
    return render(request, "users/main_page.html")  # This ensures /users/ loads base.html

def base(request):
    return render(request, "users/base.html")


def chat_page(request):
    return render(request, 'base.html')


def about_view(request):
    return render(request, "users/about.html")

def regime_page(request):
    return render(request, "regime.html")

# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import extract_from_doc, calculate_and_prompt_ai


@csrf_exempt
def upload_doc(request):
    if request.method == "POST":
        files = request.FILES.getlist("documents")
        # Do OCR or parsing
        extracted_data = {
            "salary": 1200000,
            "hra": 200000,
            "deductions": 150000
        }
        return JsonResponse(extracted_data)
    return JsonResponse({"error": "Invalid method"}, status=400)

@csrf_exempt
def regime_ai_advice(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        extracted = data.get("extracted_data", {})
        # Pass this to your AI agent
        return JsonResponse({
            "advice": "Based on your salary and deductions, the new regime saves you more tax."
        })
    return JsonResponse({"error": "Invalid method"}, status=400)












#"____________________________________________________________________________________________________________________________________________________________________"





import re
import json
from io import BytesIO
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from cloudinary.uploader import upload  # Ensure Cloudinary is configured
from django.db import transaction
from reportlab.pdfgen import canvas  # Ensure ReportLab is installed
from .models import TempUserData, UserProfile, TaxReport
from .chatbot_fsm import ChatFSM
from django.template.loader import get_template
from xhtml2pdf import pisa


@csrf_exempt
def chatbot(request):
    """Main chatbot view handling all chat interactions"""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
    # Manual authentication check for AJAX requests.
    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "Authentication required",
            "response": "❗ You must be logged in to use the chatbot. Please log in to continue.",
            "redirect": reverse("users:login")
        }, status=403)

    try:
        # Parse request data
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
        if not user_message:
            return JsonResponse({"error": "Empty message"}, status=400)

        print(f"DEBUG: User message received: '{user_message}'")
        session = request.session

        # Initialize new session if needed
        if "chat_state" not in session:
            session["chat_state"] = "full_name"
            session["temp_data"] = {}
            session.modified = True
            return JsonResponse({
                "response": "Hi! 👋 I'm your tax assistant. Let's get started."
            })

        # Get current state and handle message
        fsm = ChatFSM(session)
        current_state = fsm.get_state()
        print(f"DEBUG: Current state before handling: {current_state}")

        # Map states to their handlers
        handlers = {
            
            "full_name": handle_full_name,
            "dob": handle_DOB,
            "phone": handle_phone,
            "email": handle_email,
            "email_confirmation": handle_email_confirmation,  # ← Add this
            "address": handle_address,
            "employment": handle_employment,
            "confirm": handle_confirm,
            "ask_income": handle_ask_income,
            "income_details": handle_income_details,
            "income_confirmation": process_income_confirmation,
            "ask_deductions": process_ask_deductions,
            "deductions": handle_deductions,
            "deductions_confirmation": process_deductions_confirmation,  # New state for confirming deductions summary
            "generate_report": lambda s, m: generate_report(request, s.get("temp_data", {}))
        }

        handler = handlers.get(current_state, handle_default)
        response = handler(session, user_message)

        # If the response is already an HttpResponse instance, return it directly.
        from django.http import HttpResponse
        if isinstance(response, HttpResponse):
            return response

        print(f"DEBUG: Current state after handling: {fsm.get_state()}")
        return JsonResponse({"response": response})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        print(f"ERROR in chatbot: {str(e)}")
        # Clean up session on error
        request.session.flush()
        return JsonResponse({
            "error": "An error occurred. Please start over."
        }, status=500)




import re

def handle_full_name(session, user_message):
    """Handle name extraction without using LLM"""
    try:
        # Clean user input
        user_message = user_message.strip()
        
        # Debug print
        print(f"DEBUG: Processing name: '{user_message}'")

        # Check for common name introduction phrases
        match = re.search(r"(?:my name is|i am|this is)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)+)", user_message, re.IGNORECASE)
        if match:
            name = match.group(1)
        else:
            # If no introduction phrase, check if input is just a full name
            words = user_message.split()
            if len(words) >= 2 and all(word.isalpha() for word in words):
                name = " ".join(words)
            else:
                return "Please provide your complete full name (first and last name required)."

        # Convert name to proper case
        name = " ".join(word.title() for word in name.split())

        # Store name in session
        session["temp_data"]["full_name"] = name

        # Move to next state: set it to "dob" instead of "pan"
        fsm = ChatFSM(session)
        fsm.set_state("dob")

        return f"Thank you, {name}! What is your Date of Birth?"
    except Exception as e:
        print(f"ERROR in handle_full_name: {str(e)}")
        return "Please provide your complete full name (first and last name required)."
    
    



from datetime import datetime, date

def handle_DOB(session, user_message):
    """
    Handle DOB validation with these rules:
    1. Format must be YYYY-MM-DD
    2. Date cannot be in the future
    3. Age must be at least 18 years
    """
    try:
        # First check format
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", user_message):
            return "Invalid DOB format. Please enter your date of birth as YYYY-MM-DD"
        
        # Convert string to date object
        dob = datetime.strptime(user_message, "%Y-%m-%d").date()
        today = date.today()
        
        # Check if date is in the future
        if dob > today:
            return "Invalid DOB. Date cannot be in the future."
        
        # Calculate age
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        # Check if at least 18 years old
        if age < 18:
            return "You must be at least 18 years old to use this service."
        
        # If all validations pass, save and proceed
        session["temp_data"]["dob"] = user_message
        fsm = ChatFSM(session)
        fsm.set_state("phone")
        print(f"DEBUG: State updated to: {fsm.get_state()} and DOB saved: {session['temp_data']['dob']}")
        return "What is your phone number?"
        
    except ValueError:
        return "Invalid date. Please enter a valid date in YYYY-MM-DD format."


def handle_phone(session, user_message):
    if re.match(r"^\d{10}$", user_message):
        session["temp_data"]["phone"] = user_message
        fsm = ChatFSM(session)
        fsm.set_state("email")
        print(f"DEBUG: State updated to: {fsm.get_state()} and Phone saved: {session['temp_data']['phone']}")
        return "What is your email address?"
    return "Invalid phone number. Please enter a valid 10-digit phone number."


def handle_email(session, user_message):
    if re.match(r"[^@]+@[^@]+\.[^@]+", user_message):
        candidate_email = user_message.strip()
        # Store candidate email separately for confirmation
        session["temp_data"]["candidate_email"] = candidate_email
        fsm = ChatFSM(session)
        fsm.set_state("email_confirmation")
        print(f"DEBUG: Email candidate saved: {candidate_email}. State updated to: {fsm.get_state()}")
        return f"Should we proceed with {candidate_email} or do you want to provide another email? (yes/no)"
    return "Invalid email. Please enter a valid email address."


def handle_email_confirmation(session, user_message):
    if user_message.lower() == "yes":
        candidate_email = session["temp_data"].pop("candidate_email", None)
        if candidate_email:
            session["temp_data"]["email"] = candidate_email
        fsm = ChatFSM(session)
        fsm.set_state("address")
        print(f"DEBUG: Email confirmed: {candidate_email}. State updated to: {fsm.get_state()}")
        return "What is your address?"
    elif user_message.lower() == "no":
        # Remove candidate email and ask the user to re-enter
        session["temp_data"].pop("candidate_email", None)
        return "Okay, please provide a new email address."
    else:
        return "Please answer with 'yes' or 'no'."


def handle_address(session, user_message):
    session["temp_data"]["address"] = user_message
    fsm = ChatFSM(session)
    fsm.set_state("employment")
    print(f"DEBUG: State updated to: {fsm.get_state()} and Address saved: {session['temp_data']['address']}")
    return "Are you employed in the Government or Private sector?"


def handle_employment(session, user_message):
    if user_message.lower() in ["government", "private"]:
        session["temp_data"]["employment"] = user_message.title()
        fsm = ChatFSM(session)
        fsm.set_state("confirm")
        temp_data = session["temp_data"]
        print(f"DEBUG: State updated to: {fsm.get_state()} and Employment saved: {temp_data['employment']}")
        return (
            f"Here is your information:\n\n"
            f"✅ Name: {temp_data.get('full_name', 'N/A')}\n"
            f"✅ DOB: {temp_data.get('dob', 'N/A')}\n"
            f"✅ Phone: {temp_data.get('phone', 'N/A')}\n"
            f"✅ Email: {temp_data.get('email', 'N/A')}\n"
            f"✅ Address: {temp_data.get('address', 'N/A')}\n"
            f"✅ Employment: {temp_data.get('employment', 'N/A')}\n\n"
            f"❓ Do you confirm all this information? (yes/no)"
        )
    return "Please answer 'Government' or 'Private'."

def handle_confirm(session, user_message):
    if user_message.lower() == "yes":
        temp_data = session.get("temp_data", {})
        summary = (
            f" Name: {temp_data.get('full_name', 'N/A')}\n"
            
            f" DOB: {temp_data.get('dob', 'N/A')}\n"
            f" Phone: {temp_data.get('phone', 'N/A')}\n"
            f" Email: {temp_data.get('email', 'N/A')}\n"
            f" Address: {temp_data.get('address', 'N/A')}\n"
            f" Employment: {temp_data.get('employment', 'N/A')}\n"
        )
        fsm = ChatFSM(session)
        fsm.set_state("ask_income")
        return {
            "response": "Information confirmed. Would you like to provide your salary income details? (yes/no)",
            "blockSummary": summary,
            "blockConfirmed": True
        }
    else:
        session.flush()
        return {"response": "Let's restart. Please say 'Hi' to begin."}

def handle_default(session, user_message):
    session.flush()
    return "I'm not sure what you mean. Let's start over. Please say 'Hi'."




import re

INCOME_QUESTIONS = [
    {"key": "employer_name", "question": "Please enter your Employer's Name:"},
    {"key": "tan", "question": "Please enter your Company's TAN:"},
    {"key": "salary_income", "question": "Please enter your Gross Salary :"},
    {"key": "apply_house_rent", "question": "Do you receive House Rent Exemption (HRA)? (yes/no)"},
    {"key": "house_rent", "question": "Please enter your Monthly House Rent:"},
    {"key": "landlord_pan", "question": "Please enter your Landlord's PAN:"},
    {"key": "apply_travel_allowance", "question": "Do you have Travel Allowance(LTA)? (yes/no)"},
    {"key": "travel_allowance", "question": "Please enter your monthly Travel Allowance amount(LTA):"},
    {"key": "other_income_apply", "question": "Do you have any other source of income? (yes/no)"},
    {"key": "other_income_details", "question": "Please specify the source and amount:"},
]




def handle_ask_income(session, user_message):
    """
    Initiate income questionnaire if the user answers "yes".
    """
    try:
        user_message = user_message.strip().lower()
        fsm = ChatFSM(session)
        if user_message not in ["yes", "no"]:
            return "Please answer with 'yes' or 'no'"
        if user_message == "yes":
            # Initialize the 0-based index step and data
            fsm.set_state("income_details")
            session["income_step"] = 0
            session["income_data"] = {}
            session.modified = True
            return INCOME_QUESTIONS[0]["question"]
        else:
            fsm.set_state("generate_report")
            session.modified = True
            return ("Alright, we'll generate your tax report without income details.\n"
                    "Please wait while I prepare your report...")
    except Exception as e:
        print(f"ERROR in handle_ask_income: {str(e)}")
        return "An error occurred. Please try again with 'yes' or 'no'"






def handle_income_details(session, user_message):
    """
    Process the income questionnaire one question at a time.
    """
    if "income_step" not in session:
        session["income_step"] = 0
        session["income_data"] = {}

    step = session["income_step"]
    income_data = session.get("income_data", {})

    if step >= len(INCOME_QUESTIONS):
        return "❌ Unexpected error: Step out of range. Please restart."

    # Get current question
    current_question = INCOME_QUESTIONS[step]
    current_key = current_question["key"]
    answer = user_message.strip()

    # Process answer based on type
    if current_key in ["salary_income", "house_rent", "travel_allowance"]:
        try:
            amount = float(answer.replace(',', ''))
            if amount <= 0:
                return f"⚠️ {current_question['question']} must be a positive number. Try again."
            income_data[current_key] = amount
        except ValueError:
            return f"❌ Invalid input! Please enter a numeric value for {current_question['question']}."

    elif current_key in ["apply_house_rent", "apply_travel_allowance", "other_income_apply"]:
        if answer.lower() not in ["yes", "no"]:
            return "❌ Invalid input! Please answer with 'yes' or 'no'."
        income_data[current_key] = answer.lower()

    elif current_key == "employer_name":
        if len(answer) < 3:
            return "❌ Employer name must be at least 3 characters long."
        income_data[current_key] = answer  

    elif current_key == "tan":
        answer = answer.upper().strip()
        if not re.match(r"^[A-Z]{4}\d{5}[A-Z]$", answer):
            return ("❌ Invalid TAN format! \n"
                    "✅ Format: AAAA99999A (4 letters, 5 digits, 1 letter). \n"
                    "📌 Example: MUMB12345W\n"
                    "🔄 Please enter a valid TAN:")
        income_data[current_key] = answer


    elif current_key == "landlord_pan":
        answer = answer.upper().strip()
        if not re.match(r"^[A-Z]{5}\d{4}[A-Z]$", answer):
            return "❌ Invalid PAN format! Format: AAAAA9999A"
        income_data[current_key] = answer

# PAN block is removed so no vakue to compare user PAN 

    elif current_key == "other_income_details":
        parts = answer.split()
        if len(parts) < 2:
            return "❌ Please specify both the source and the amount (e.g., freelance 150000)."
        source = " ".join(parts[:-1])
        try:
            amount = float(parts[-1].replace(',', ''))
            if amount <= 0:
                return "❌ Income amount must be a positive number."
            income_data["other_income_source"] = source
            income_data["other_income_amount"] = amount
        except ValueError:
            return "❌ Invalid input! Please enter a valid amount (e.g., freelance 150000)."
    else:
        income_data[current_key] = answer  # Store any other answers normally

    # Determine next step based on conditions
    if current_key == "apply_house_rent" and income_data.get("apply_house_rent") == "no":
        step = next(i for i, q in enumerate(INCOME_QUESTIONS) if q["key"] == "apply_travel_allowance")  

    elif current_key == "house_rent":
        try:
            rent = float(income_data.get("house_rent", 0))
            # Check if monthly rent exceeds 50,000; if so, warn the user.
            if rent > 50000:
                return "Please note that you are supposed to deduct TDA."  # Warning message

            annual_rent = rent * 12

            if annual_rent > 100000:  # If annual rent is greater than ₹100,000, ask for landlord PAN
                step += 1
            else:  # Otherwise, skip to the next relevant question
                step = next(i for i, q in enumerate(INCOME_QUESTIONS) if q["key"] == "apply_travel_allowance")
        except ValueError:
            return "❌ Invalid rent amount. Please enter a valid number."


    elif current_key == "apply_travel_allowance" and income_data.get("apply_travel_allowance") == "no":
        step = next(i for i, q in enumerate(INCOME_QUESTIONS) if q["key"] == "other_income_apply")  

    elif current_key == "other_income_apply" and income_data.get("other_income_apply") == "no":
        step = len(INCOME_QUESTIONS)  

    else:
        step += 1  

    # Update session with new step and data.
    session["income_step"] = step
    session["income_data"] = income_data
    session.modified = True
    print(f"DEBUG: Updated income data: {session['income_data']}")  

    # If questionnaire is complete, generate summary
    if step >= len(INCOME_QUESTIONS):
        fsm = ChatFSM(session)
        fsm.set_state("income_confirmation")
        return format_income_summary(income_data)

    return INCOME_QUESTIONS[step]["question"]  # Ask the next question







def format_income_summary(income_data):
    """
    Format the collected income data and present a confirmation summary.
    """
    try:
        summary = "📊 Tax Return Details Summary\n" + "=" * 40 + "\n\n"
        summary += "👔 Employment Information\n" + "-" * 25 + "\n"
        summary += f"🏢 Employer: {income_data.get('employer_name', 'N/A')}\n"
        print(f"DEBUG: Summary employer name: {income_data.get('employer_name')}")

        summary += f"📝 TAN: {income_data.get('tan', 'N/A')}\n\n"
        summary += "💰 Income Details\n" + "-" * 20 + "\n"
        try:
            salary = float(income_data.get('salary_income', 0))
            summary += f"📈 Annual Salary: ₹{salary:,.2f}\n"
        except (ValueError, TypeError):
            summary += "📈 Annual Salary: Not provided\n"
        if income_data.get('apply_house_rent') == 'yes':
            summary += "\n🏠 House Rent Details\n" + "-" * 23 + "\n"
            try:
                rent = float(income_data.get('house_rent', 0))
                summary += f"💵 Monthly Rent: ₹{rent:,.2f}\n"
                summary += f"📋 Landlord PAN: {income_data.get('landlord_pan', 'N/A')}\n"
            except (ValueError, TypeError):
                summary += "💵 Monthly Rent: Invalid amount provided\n"
        if income_data.get('apply_travel_allowance') == 'yes':
            summary += "\n🚗 Travel Allowance\n" + "-" * 20 + "\n"
            try:
                travel = float(income_data.get('travel_allowance', 0))
                summary += f"🎫 Annual Amount: ₹{travel:,.2f}\n"
            except (ValueError, TypeError):
                summary += "🎫 Annual Amount: Invalid amount provided\n"
        if income_data.get('other_income_apply') == 'yes':
            summary += "\n💵 Other Income Sources\n" + "-" * 23 + "\n"
            summary += (f"📝 Details: {income_data.get('other_income_source', 'N/A')} "
                        f"₹{float(income_data.get('other_income_amount', 0)):,.2f}\n")
        try:
            total = float(income_data.get('salary_income', 0))
            if income_data.get('apply_house_rent') == 'yes':
                total += float(income_data.get('house_rent', 0)) * 12
            if income_data.get('apply_travel_allowance') == 'yes':
                total += float(income_data.get('travel_allowance', 0))
            if income_data.get('other_income_apply') == 'yes':
                total += float(income_data.get('other_income_amount', 0))
            summary += "\n💼 Total Annual Income\n" + "-" * 23 + "\n"
            summary += f"📊 Total: ₹{total:,.2f}\n"
        except (ValueError, TypeError):
            summary += "\n⚠️ Could not calculate total due to invalid amounts\n"
        summary += "\n" + "=" * 40 + "\n"
        summary += "✅ Is this information correct? (yes/no)"
        return summary
    except Exception as e:
        print(f"Error formatting income summary: {str(e)}")
        return ("⚠️ Error generating summary. Please check your inputs.\n\n"
                "Is the information you provided correct? (yes/no)")




def process_income_confirmation(session, user_message):
    """
    Process user's confirmation of income details.
    If confirmed, merge the income data into temp_data and ask about deductions.
    Otherwise, start over.
    """
    try:
        if user_message.lower() not in ["yes", "no"]:
            return {"response": "Please answer with 'yes' or 'no'."}
        if user_message.lower() == "yes":
            income_data = session.get("income_data", {})
            try:
                income_data["salary_income"] = float(income_data.get("salary_income", 0))
                income_data["house_rent"] = float(income_data.get("house_rent", 0))
                income_data["travel_allowance"] = float(income_data.get("travel_allowance", 0))
            except ValueError:
                return {"response": "Invalid numeric values in income data. Please start over."}
            temp_data = session.get("temp_data", {})
            temp_data.update(income_data)
            session["temp_data"] = temp_data
            session.pop("income_step", None)
            session.pop("income_data", None)
            session.modified = True
            fsm = ChatFSM(session)

            # Now we ask about deductions instead of report generation directly.
            fsm.set_state("ask_deductions")
            summary = format_income_summary(income_data)
            return {
                "response": "✅ Income details confirmed!\n\nWould you like to provide deduction details to help reduce your tax payable? (yes/no)",
                "blockSummary": summary,
                "blockConfirmed": True
            }
        else:
            session.pop("income_step", None)
            session.pop("income_data", None)
            session.modified = True
            return {"response": f"🔄 Let's re-enter your income details.\n\n{INCOME_QUESTIONS[0]['question']}"}
    except Exception as e:
        print(f"ERROR in process_income_confirmation: {str(e)}")
        session.pop("income_step", None)
        session.pop("income_data", None)
        session.modified = True
        return {"response": "An error occurred. Let's start the income details again."}





# Deductions 


import re
from django.http import JsonResponse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Define the deduction questions in order.
DEDUCTION_QUESTIONS = [
    {"key": "has_epf", "question": "Do you have EPF? (yes/no)"},
    {"key": "epf_amount", "question": "What is the amount of EPF?"},
    
    {"key": "has_life_insurance", "question": "Do you have Life Insurance? (yes/no)"},
    {"key": "life_insurance_amount", "question": "What is the amount of Life Insurance Premium?"},

    {"key": "has_mf", "question": "Do you invest in Mutual Funds? (yes/no)"},
    {"key": "mf_value", "question": "What is the value of your Mutual Fund investments?"},

    {"key": "has_ppf", "question": "Do you invest in Public Provident Fund (PPF)? (yes/no)"},
    {"key": "ppf_value", "question": "What is the value of your PPF investments?"},

    {"key": "has_nsc", "question": "Do you have National Saving Certificate (NSC)? (yes/no)"},
    {"key": "nsc_amount", "question": "What is the amount invested in NSC?"},

    {"key": "has_home_loan", "question": "Do you have a home loan? (yes/no)"},
    {"key": "home_loan_amount", "question": "What is the amount of your home loan?"},
    {"key": "home_loan_tenure", "question": "What is the tenure of your home loan (in years)?"},
    {"key": "home_loan_interest", "question": "What is the interest paid on the principal of your home loan?"},

    {"key": "has_child_tuition", "question": "Do you pay for child tuition fees? (yes/no)"},
    {"key": "child_tuition_amount", "question": "What is the amount of child tuition fees?"},

    {"key": "has_other_80c", "question": "Do you invest in any other activities under 80C? (yes/no)"},
    {"key": "other_80c_details", "question": "Please specify the activity and the amount invested (e.g., 'activity 10000')."},

    # Section 80D: Health Insurance
    {"key": "has_health_self", "question": "Do you have health insurance for self/family? (yes/no)"},
    {"key": "health_self_amount", "question": "What is the premium amount for self/family?"},

    {"key": "has_health_parents", "question": "Do you have health insurance for Parents? (yes/no)"},
    {"key": "health_parents_amount", "question": "What is the premium amount for your parents?"},

    # Section 80E: Education Loan Interest
    {"key": "has_edu_loan", "question": "Do you have an education loan? (yes/no)"},
    {"key": "edu_loan_interest", "question": "What is the amount of interest paid for the education loan?"},

    # Section CCD(1B): NPS
    {"key": "has_nps", "question": "Do you invest in the National Pension Scheme (NPS)? (yes/no)"},
    {"key": "nps_amount", "question": "What is the amount invested in NPS?"},

    # Interest on Savings
    {"key": "has_interest_savings", "question": "Did you earn interest on savings? (yes/no)"},
    {"key": "interest_savings", "question": "What is the amount of interest earned on savings?"},

    # FD Interest for Senior Citizens
    {"key": "has_interest_fd", "question": "Do you have Fixed Deposits for senior citizens? (yes/no)"},
    {"key": "interest_fd", "question": "What is the amount of interest earned on FD?"},

    # Dividend Income
    {"key": "has_dividend", "question": "Did you earn dividend income? (yes/no)"},
    {"key": "dividend_income", "question": "What is the amount of dividend income earned?"}
]

# Set up a mapping for yes/no conditional skips.
# For example, if "has_epf" is "no", skip the very next question.
SKIP_MAP = {
    "has_epf": 1,
    "has_life_insurance": 1,
    "has_mf": 1,
    "has_ppf": 1,
    "has_nsc": 1,
    "has_home_loan": 3,  # Skip home_loan_amount, home_loan_tenure, home_loan_interest.
    "has_child_tuition": 1,
    "has_other_80c": 1,
    "has_health_self": 1,
    "has_health_parents": 1,
    "has_edu_loan": 1,
    "has_nps": 1,
    "has_interest_savings": 1,
    "has_interest_fd": 1,
    "has_dividend": 1
}


def process_ask_deductions(session, user_message):
    """
    After income details are confirmed, ask if the user wants to provide deduction details.
    If yes, start the deductions questionnaire; if no, proceed to report generation.
    """
    if user_message.lower() not in ["yes", "no"]:
        return "Please answer with 'yes' or 'no'."
    fsm = ChatFSM(session)
    if user_message.lower() == "yes":
        fsm.set_state("deductions")
        # Initialize the deductions questionnaire tracking.
        session["deduc_step"] = 0
        session["deductions_data"] = {}
        session.modified = True
        return DEDUCTION_QUESTIONS[0]["question"]
    else:
        fsm.set_state("generate_report")
        return ("Alright, proceeding without deductions.\nGenerating your tax report now...")


def handle_deductions(session, user_message):
    """
    Process the deduction questionnaire one question at a time.
    Uses 0-based indexing. Conditional questions are skipped based on yes/no answers.
    """
    if "deduc_step" not in session:
        session["deduc_step"] = 0
        session["deductions_data"] = {}
    
    step = session["deduc_step"]
    deductions_data = session.get("deductions_data", {})

    if step >= len(DEDUCTION_QUESTIONS):
        return "❌ Unexpected error: Step out of range. Please restart the deductions process."
    
    # Get the current question.
    current_question = DEDUCTION_QUESTIONS[step]
    current_key = current_question["key"]
    answer = user_message.strip()
    
    # Process based on type.
    # For yes/no fields.
    if current_key.startswith("has_"):
        if answer.lower() not in ["yes", "no"]:
            return "❌ Invalid input! Please answer with 'yes' or 'no'."
        deductions_data[current_key] = answer.lower()
    # For numeric inputs.
    elif current_key in [
        "epf_amount", "life_insurance_amount", "mf_value", "ppf_value", "nsc_amount",
        "home_loan_amount", "home_loan_tenure", "home_loan_interest", "child_tuition_amount",
        "health_self_amount", "health_parents_amount", "edu_loan_interest", "nps_amount",
        "interest_savings", "interest_fd", "dividend_income"
    ]:
        try:
            num = float(answer.replace(',', ''))
            if num < 0:
                return f"⚠️ {current_question['question']} must be a positive number. Try again."
            deductions_data[current_key] = num
        except ValueError:
            return f"❌ Invalid input! Please enter a numeric value for {current_question['question']}."
    else:
        # Otherwise, store text response (for instance, for other_80c_details).
        deductions_data[current_key] = answer

    # Determine next step.
    # If the current question is a yes/no conditional question and answer is "no", skip its dependent question(s).
    if current_key in SKIP_MAP and deductions_data[current_key] == "no":
        step += SKIP_MAP[current_key] + 1
    else:
        step += 1

    # Update session.
    session["deduc_step"] = step
    session["deductions_data"] = deductions_data
    session.modified = True
    print(f"DEBUG: Updated deductions data: {session['deductions_data']}")

    # If the questionnaire is complete, generate summary.
    # If the questionnaire is complete, generate summary.
    if step >= len(DEDUCTION_QUESTIONS):
        # Instead of returning an error, update the state so that further input
        # is handled by the deductions confirmation handler.
        fsm = ChatFSM(session)
        fsm.set_state("deductions_confirmation")
        return format_deductions_summary(deductions_data)
        
    # Otherwise, ask next question.
    return DEDUCTION_QUESTIONS[step]["question"]


def format_deductions_summary(data):
    """
    Compute deduction amounts using the rules provided and format a summary.
    Rules:
      Deduction_A (80C) = EPF + Life Insurance + MF + PPF + NSC + (home loan amount, if applicable) +
                          child tuition fees + others (from other_80c_details; assume that the numeric value is provided).
      Cap Deduction_A at 150000.
      
      Deduction_B1 = min(health_self_amount, 25000)
      Deduction_B2 = min(health_parents_amount, 50000)
      Deduction_B = Deduction_B1 + Deduction_B2
      
      Deduction_C (80E) = edu_loan_interest
      
      Deduction_D (NPS) = min(nps_amount, 50000)
      
      Deduction_H = min(home_loan_interest, 200000)  [if home loan exists]
      
      Deduction_F = min(interest_savings, 10000)
      Deduction_G = min(interest_fd, 50000)
      
      Income_on_savings = interest_savings + interest_fd
      
      Dividend Income = dividend_income (if provided)
      
      Primary Income = (proprietary income should be provided earlier) + Income_on_savings + Dividend Income
      
      (For this summary, we display only the deductions.)
    """
    try:
        # 80C values:
        epf = data.get("epf_amount", 0) if data.get("has_epf", "no") == "yes" else 0
        life = data.get("life_insurance_amount", 0) if data.get("has_life_insurance", "no") == "yes" else 0
        mf = data.get("mf_value", 0) if data.get("has_mf", "no") == "yes" else 0
        ppf = data.get("ppf_value", 0) if data.get("has_ppf", "no") == "yes" else 0
        nsc = data.get("nsc_value", 0) if data.get("has_nsc", "no") == "yes" else 0
        home_loan = data.get("home_loan_principal", 0) if data.get("has_home_loan", "no") == "yes" else 0
        child_tuition = data.get("child_tuition_fees", 0) if data.get("has_child_tuition", "no") == "yes" else 0
        other_80C = data.get("other_80C_amount", 0) if data.get("has_other_80C", "no") == "yes" else 0

        deduction_A = epf + life + mf + ppf + nsc + home_loan + child_tuition + other_80C
        deduction_A = min(deduction_A, 150000)

        # 80D (Health Insurance):
        health_self = data.get("health_self_amount", 0) if data.get("has_health_self", "no") == "yes" else 0
        health_parents = data.get("health_parents_amount", 0) if data.get("has_health_parents", "no") == "yes" else 0
        deduction_B1 = min(health_self, 25000)
        deduction_B2 = min(health_parents, 50000)
        deduction_B = deduction_B1 + deduction_B2

        # 80E (Education Loan)
        edu_loan_interest = data.get("education_loan_interest", 0) if data.get("has_edu_loan", "no") == "yes" else 0
        deduction_C = edu_loan_interest

        # NPS (CCD(1B))
        nps_amt = data.get("nps_amount", 0) if data.get("has_nps", "no") == "yes" else 0
        deduction_D = min(nps_amt, 50000)

        # Interest on savings & FD interest:
        interest_savings = data.get("interest_savings", 0) if data.get("has_interest_savings", "no") == "yes" else 0
        deduction_F = min(interest_savings, 10000)
        interest_fd = data.get("interest_fd", 0) if data.get("has_interest_fd", "no") == "yes" else 0
        deduction_G = min(interest_fd, 50000)

        # Dividend income (if any)
        dividend_income = data.get("dividend_income", 0) if data.get("has_dividend", "no") == "yes" else 0

         # Build thorough summary string:
        summary = (
            "📊 Deduction Summary\n" + "="*40 + "\n\n" +
            "Section 80C:\n" +
            f"  EPF: ₹{epf:,.2f}\n" +
            f"  Life Insurance: ₹{life:,.2f}\n" +
            f"  Mutual Funds: ₹{mf:,.2f}\n" +
            f"  PPF: ₹{ppf:,.2f}\n" +
            f"  NSC: ₹{nsc:,.2f}\n" +
            f"  Home Loan Principal: ₹{home_loan:,.2f}\n" +
            f"  Child Tuition Fees: ₹{child_tuition:,.2f}\n" +
            f"  Other 80C Amount: ₹{other_80C:,.2f}\n" +
            f"  Total Deduction A (capped at ₹150,000): ₹{deduction_A:,.2f}\n\n" +
            "Section 80D (Health Insurance):\n" +
            f"  Health Insurance (Self): ₹{health_self:,.2f} (Capped: ₹{deduction_B1:,.2f})\n" +
            f"  Health Insurance (Parents): ₹{health_parents:,.2f} (Capped: ₹{deduction_B2:,.2f})\n" +
            f"  Total Deduction B: ₹{deduction_B:,.2f}\n\n" +
            "Section 80E (Education Loan):\n" +
            f"  Education Loan Interest: ₹{edu_loan_interest:,.2f}\n" +
            f"  Deduction C: ₹{deduction_C:,.2f}\n\n" +
            "Section CCD(1B) (NPS Investment):\n" +
            f"  NPS Amount: ₹{nps_amt:,.2f} (Capped: ₹{deduction_D:,.2f})\n\n" +
            "Investment Deductions:\n" +
            f"  Interest on Savings: ₹{interest_savings:,.2f} (Capped: ₹{deduction_F:,.2f})\n" +
            f"  FD Interest: ₹{interest_fd:,.2f} (Capped: ₹{deduction_G:,.2f})\n" +
            f"  Dividend Income: ₹{dividend_income:,.2f}\n\n" +
            "="*40 + "\n" +
            "Please confirm these deductions. (yes/no)"
        )
        return summary
    except Exception as e:
        logger.error(f"Error formatting deductions summary: {str(e)}")
        return "Error generating deductions summary. Please re-enter your details."




def process_deductions_confirmation(session, user_message):
    """
    Process confirmation of the deductions details.
    If confirmed, merge the deductions data into temp_data for further processing.
    """

    try:
        if user_message.lower() not in ["yes", "no"]:
            return {"response": "Please answer with 'yes' or 'no'."}
        if user_message.lower() == "yes":
            deductions_data = session.get("deductions_data", {})
            temp_data = session.get("temp_data", {})
            temp_data.update(deductions_data)
            session["temp_data"] = temp_data
            session.pop("deduc_step", None)
            session.pop("deductions_data", None)
            session.modified = True
            fsm = ChatFSM(session)
            fsm.set_state("generate_report")
            summary = format_deductions_summary(deductions_data)
            return {
                "response": "✅ Deductions confirmed!\nGenerating your tax report now...",
                "blockSummary": summary,
                "blockConfirmed": True
            }
        else:
            session.pop("deduc_step", None)
            session.pop("deductions_data", None)
            session.modified = True
            return {"response": "🔄 Let's re-enter your deduction details.\n" + DEDUCTION_QUESTIONS[0]["question"]}
    except Exception as e:
        logger.error(f"Error in process_deductions_confirmation: {str(e)}")
        session.pop("deduc_step", None)
        session.pop("deductions_data", None)
        session.modified = True
        return {"response": "An error occurred. Please re-enter your deduction details."}





def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        # You can add more validation here
        send_mail(
            f'Contact Form Submission from {name}',
            f'Email: {email}\nContact: {contact}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
        )
        messages.success(request, 'Thank you for contacting us!')
        return redirect('home')
    return redirect('home')












from django.db import transaction
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from cloudinary.uploader import upload
from django.http import JsonResponse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def generate_report(request, temp_data):
    """
    Generate a tax report PDF from user-provided data.
    This version includes basic details, income details, and individual deduction fields.
    """
    try:
        with transaction.atomic():
            def safe_float(value, default=0.0):
                try:
                    return float(value)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Safe conversion failed for value '{value}': {str(e)}")
                    return default

            # Create basic data record for the user.
            basic_data = TempUserData.objects.create(
                user=request.user,
                full_name=temp_data.get('full_name', '').strip(),
                
                dob=temp_data.get('dob', '2000-01-01'),
                phone=temp_data.get('phone', '').strip(),
                email=temp_data.get('email', '').strip(),
                address=temp_data.get('address', '').strip(),
                employment=temp_data.get('employment', '').strip()
            )

            # Create income details record.
            income_details = TempIncomeDetails.objects.create(
                user=request.user,
                employer_name=temp_data.get('employer_name', '').strip(),
                tan=temp_data.get('tan', '').strip().upper(),
                salary_income=safe_float(temp_data.get('salary_income', 0)),
                house_rent_applied=(temp_data.get('apply_house_rent', '').lower() == 'yes'),
                house_rent_amount=safe_float(temp_data.get('house_rent', 0)),
                landlord_pan=temp_data.get('landlord_pan', '').strip().upper(),
                travel_allowance_applied=(temp_data.get('apply_travel_allowance', '').lower() == 'yes'),
                travel_allowance_amount=safe_float(temp_data.get('travel_allowance', 0)),
                other_income_applied=(temp_data.get('other_income_apply', '').lower() == 'yes'),
                other_income_source=temp_data.get('other_income_source', '').strip(),
                other_income_amount=safe_float(temp_data.get('other_income_amount', 0))
            )

            # Set fallbacks for other income.
            other_income_source = income_details.other_income_source or "N/A"
            other_income_amount = income_details.other_income_amount if income_details.other_income_amount > 0 else 0

            # Compute individual deduction values from temp_data if available.
            # (These values should have been saved in temp_data following the deductions questionnaire.)
            # 80C values:
            epf = safe_float(temp_data.get("epf_amount", 0)) if temp_data.get("has_epf", "no") == "yes" else 0
            life = safe_float(temp_data.get("life_insurance_amount", 0)) if temp_data.get("has_life_insurance", "no") == "yes" else 0
            mf = safe_float(temp_data.get("mf_value", 0)) if temp_data.get("has_mf", "no") == "yes" else 0
            ppf = safe_float(temp_data.get("ppf_value", 0)) if temp_data.get("has_ppf", "no") == "yes" else 0
            nsc = safe_float(temp_data.get("nsc_amount", 0)) if temp_data.get("has_nsc", "no") == "yes" else 0
            home_loan = safe_float(temp_data.get("home_loan_amount", 0)) if temp_data.get("has_home_loan", "no") == "yes" else 0
            child_tuition = safe_float(temp_data.get("child_tuition_amount", 0)) if temp_data.get("has_child_tuition", "no") == "yes" else 0
            other_80C = safe_float(temp_data.get("other_80C_amount", 0)) if temp_data.get("has_other_80C", "no") == "yes" else 0
            deduction_A = min(epf + life + mf + ppf + nsc + home_loan + child_tuition + other_80C, 150000)

            # 80D (Health Insurance):
            health_self = safe_float(temp_data.get("health_self_amount", 0)) if temp_data.get("has_health_self", "no") == "yes" else 0
            health_parents = safe_float(temp_data.get("health_parents_amount", 0)) if temp_data.get("has_health_parents", "no") == "yes" else 0
            deduction_B1 = min(health_self, 25000)
            deduction_B2 = min(health_parents, 50000)
            deduction_B = deduction_B1 + deduction_B2

            # 80E (Education Loan)
            edu_loan_interest = safe_float(temp_data.get("edu_loan_interest", 0)) if temp_data.get("has_edu_loan", "no") == "yes" else 0
            deduction_C = edu_loan_interest

            # CCD(1B) (NPS)
            nps_amt = safe_float(temp_data.get("nps_amount", 0)) if temp_data.get("has_nps", "no") == "yes" else 0
            deduction_D = min(nps_amt, 50000)

            # Investment deductions:
            interest_savings = safe_float(temp_data.get("interest_savings", 0)) if temp_data.get("has_interest_savings", "no") == "yes" else 0
            deduction_F = min(interest_savings, 10000)
            interest_fd = safe_float(temp_data.get("interest_fd", 0)) if temp_data.get("has_interest_fd", "no") == "yes" else 0
            deduction_G = min(interest_fd, 50000)
            dividend_income = safe_float(temp_data.get("dividend_income", 0)) if temp_data.get("has_dividend", "no") == "yes" else 0

            # Merge all details into one dictionary.
            # Convert house rent to annual.
            # Merge all details into one dictionary.
            merged_data = {
                'id': basic_data.id,
                'full_name': basic_data.full_name,
                
                'dob': basic_data.dob,
                'phone': basic_data.phone,
                'email': basic_data.email,
                'address': basic_data.address,
                'employment': basic_data.employment,
                # Income details:
                'employer_name': income_details.employer_name,
                'tan': income_details.tan,
                'salary_income': income_details.salary_income,
                'house_rent': income_details.house_rent_amount * 12,  # Annual House Rent
                'landlord_pan': income_details.landlord_pan,
                'travel_allowance': income_details.travel_allowance_amount,
                'other_income_source': other_income_source,
                'other_income_amount': other_income_amount,
                # Deductions:
                'deductions_80C': {
                    'epf': epf,
                    'life_insurance': life,
                    'mutual_funds': mf,
                    'ppf': ppf,
                    'nsc': nsc,
                    'home_loan_principal': home_loan,
                    'child_tuition': child_tuition,
                    'other_80C': other_80C,
                    'total_deduction_A': deduction_A,
                },
                'deductions_80D': {
                    'health_insurance_self': health_self,
                    'capped_self': deduction_B1,
                    'health_insurance_parents': health_parents,
                    'capped_parents': deduction_B2,
                    'total_deduction_B': deduction_B,
                },
                'deductions_80E': {
                    'education_loan_interest': edu_loan_interest,
                    'deduction_C': deduction_C,
                },
                'ccd_1B': {
                    'nps_amount': nps_amt,
                    'deduction_D': deduction_D,
                },
                'investment_deductions': {
                    'interest_on_savings': interest_savings,
                    'capped_savings': deduction_F,
                    'fd_interest': interest_fd,
                    'capped_fd': deduction_G,
                    'dividend_income': dividend_income,
                }
            }

            file_name = f"tax_report_{request.user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            template = get_template('users/report.html')
            context = {
                'user': request.user,
                'temp_data': merged_data,
                'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            html = template.render(context)
            result = BytesIO()
            pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=result)
            if pdf.err:
                raise Exception(f"PDF Generation Error: {pdf.err}")
            result.seek(0)
            
            cloudinary_response = upload(
                result, 
                resource_type="raw", 
                public_id=file_name,
                folder="tax_reports"
            )
            secure_url = cloudinary_response.get("secure_url")
            if not secure_url:
                raise Exception("Failed to get secure URL from Cloudinary")
            
            basic_data.pdf_url = secure_url
            basic_data.save()
            
            UserProfile.objects.update_or_create(
                user=request.user,
                defaults={
                    'full_name': basic_data.full_name,
                    
                    'dob': basic_data.dob,
                    'phone': basic_data.phone,
                    'email': basic_data.email,
                    'address': basic_data.address,
                    'employment': basic_data.employment
                }
            )
            TaxReport.objects.create(
                user=request.user,
                pdf_url=basic_data.pdf_url,
            )
            
            logger.info(f"PDF generated and uploaded successfully: {basic_data.pdf_url}")
            return JsonResponse({"response": basic_data.pdf_url})
    
    except ValueError as e:
        logger.error(f"Value Error in generate_report: {str(e)}")
        return JsonResponse({"error": "Value error during report generation"}, status=500)
    except Exception as e:
        logger.error(f"Error in generate_report: {str(e)}")
        return JsonResponse({"error": "Error generating report"}, status=500)