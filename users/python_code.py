
"""

import re
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import TempUserData

@login_required
def chatbot(request):
    user_message = request.GET.get("message", "").strip().lower()
    session = request.session

    # Initialize session if not present
    if "chat_state" not in session:
        session["chat_state"] = "greeting"
        session["temp_data"] = {}
        session.modified = True

    # Determine current state
    chat_state = session["chat_state"]

    # Route to the appropriate handler
    if chat_state == "greeting":
        response = handle_greeting(session, user_message)
    if chat_state == "full_name":
        response = handle_full_name(session, user_message)
    if chat_state == "pan":
        response = handle_pan(session, user_message)
    if chat_state == "uid":
        response = handle_uid(session, user_message)
    if chat_state == "DOB":
        response = handle_DOB(session, user_message)
    if chat_state == "phone":
        response = handle_phone(session, user_message)        
    if chat_state == "email":
        response = handle_email(session, user_message)
    if chat_state == "address":
        response = handle_address(session, user_message)
    if chat_state == "employment":
        response = handle_employment(session, user_message)    
    if chat_state == "confirm":
        response = handle_confirm(session, user_message)

    else:
        response = "I'm not sure what you mean. Let's start over. Please say 'Hi'."

    return JsonResponse({"response": response})


def handle_greeting(session, user_message):
    # Split user message into words; assume user message is already lower case.
    words = user_message.split()
    greetings = {"hi", "hello", "hii", "hey", "hola"}
    # Check if any word exactly matches one of our greetings.
    if any(word in greetings for word in words):
        session["chat_state"] = "full_name"
        session.modified = True
        return "What is your full name?"
    return "Please say 'Hi' to start."


def handle_full_name(session, user_message):
    # Save full name and update state to ask for PAN.
    session["temp_data"]["full_name"] = user_message.title()
    session["chat_state"] = "pan"
    session.modified = True
    return f"Hi {user_message.title()}! What is your PAN number?"


def handle_pan(session, user_message):
    # Verify PAN length; update state if valid.
    if len(user_message) == 10:
        session["temp_data"]["pan"] = user_message.upper()
        session["chat_state"] = "uid"  # Proceed to next state; define handle_uid similarly.
        session.modified = True
        return "What is your 12-digit UID (Aadhar) number?"
    return "Invalid PAN. Please enter a valid 10-character PAN number."

def handle_uid(session, user_message):
    # Verify UID length; update state if valid.
    if len(user_message) == 12:
        session["temp_data"]["uid"] = user_message
        session["chat_state"] = "DOB"  # Proceed to next state; define handle_phone similarly.
        session.modified = True
        return "What is your Date of Birth ?"
    return "Invalid UID. Please enter a valid 12-digit UID number."

def handle_DOB(session, user_message):
    # Verify DOB format; update state if valid.
    if re.match(r"\d{2}-\d{2}-\d{4}", user_message):
        session["temp_data"]["DOB"] = user_message
        session["chat_state"] = "phone"  # Proceed to next state; define handle_phone similarly.
        session.modified = True
        return "What is your phone number?"
    return "Invalid DOB. Please enter your date of birth in the format 'DD-MM-YYYY'."

def handle_phone(session, user_message):
    # Verify phone number format; update state if valid.
    if re.match(r"\d{10}", user_message):
        session["temp_data"]["phone"] = user_message
        session["chat_state"] = "email"  # Proceed to next state; define handle_email similarly.
        session.modified = True
        return "What is your email address?"
    return "Invalid phone number. Please enter a valid 10-digit phone number."

def handle_email(session, user_message):
    # Verify email format; update state if valid.
    if re.match(r"[^@]+@[^@]+\.[^@]+", user_message):
        session["temp_data"]["email"] = user_message
        session["chat_state"] = "address"  # Proceed to next state; define handle_address similarly.
        session.modified = True
        return "What is your address?"
    return "Invalid email. Please enter a valid email address."

def handle_address(session, user_message):
    # Save address and update state to ask for employment details.
    session["temp_data"]["address"] = user_message
    session["chat_state"] = "employment"
    session.modified = True
    return "What is your employment status?"


# Handle Employment
def handle_employment(session, user_message):
    if user_message.lower() in ["government", "private"]:
        session["temp_data"]["employment"] = user_message.title()
        session["chat_state"] = "confirm"
        session.modified = True
        temp_data = session["temp_data"]
        return (
            f"Here is your information:\n\n"
            f"✅ Name: {temp_data.get('full_name', 'N/A')}\n"
            f"✅ PAN: {temp_data.get('pan', 'N/A')}\n"
            f"✅ UID: {temp_data.get('uid', 'N/A')}\n"
            f"✅ DOB: {temp_data.get('dob', 'N/A')}\n"
            f"✅ Phone: {temp_data.get('phone', 'N/A')}\n"
            f"✅ Email: {temp_data.get('email', 'N/A')}\n"
            f"✅ Address: {temp_data.get('address', 'N/A')}\n"
            f"✅ Employment: {temp_data.get('employment', 'N/A')}\n\n"
            f"❓ Do you confirm all this information? (yes/no)"
        )
    return "Please answer 'Government' or 'Private'."


# Handle Confirmation
def handle_confirm(session, user_message):
    if user_message.lower() == "yes":
        # For example, save to your temporary model
        TempUserData.objects.create(**session["temp_data"], user=session.get("user"))
        session["chat_state"] = "done"
        session.modified = True
        return "Your data has been saved! 🎉"
    session["chat_state"] = "greeting"
    session.modified = True
    return "Let's restart. Please say 'Hi' to begin."


# Default handler
def handle_default(session, user_message):
    return "I'm not sure what you mean. Let's start over. Please say 'Hi'."





"""








import re

# Dummy ChatFSM mimicking your production class.
class ChatFSM:
    states = ["greeting", "full_name", "pan", "uid", "dob", "phone", "email", "address", "employment", "confirm", "done"]
    
    def __init__(self, session):
        self.session = session
        if "chat_state" not in self.session:
            self.session["chat_state"] = self.states[0]
    
    def set_state(self, state):
        if state in self.states:
            self.session["chat_state"] = state
            
    def get_state(self):
        return self.session.get("chat_state")

# Dummy extraction function that returns "greeting" when a common greeting is detected.
def extract_data(text):
    normalized = re.sub(r'[^\w\s]', '', text.strip().lower())
    if normalized in ["hi", "hello", "hey", "hii", "hola"]:
        return "greeting"
    return ""

# Your handle_greeting implementation:
def handle_greeting(session, user_message):
    # Use the dummy NLP function and fallback regex
    intent = extract_data(user_message)
    normalized = re.sub(r'[^\w\s]', '', user_message.strip().lower())
    regex_found = re.search(r'\b(hi|hello|hii|hey|hola)\b', normalized)
    
    if intent == "greeting" or regex_found:
        fsm = ChatFSM(session)
        fsm.set_state("full_name")
        return "What is your full name?"
    return "Please say 'Hi' to start."

# Test harness for the function
if __name__ == '__main__':
    # Mimic an empty session dict.
    session = {}
    
    user_message = input("Enter greeting message: ")
    response = handle_greeting(session, user_message)
    print("Response:", response)
    print("Session state:", session.get("chat_state"))













