from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User

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
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, f"Account created! Welcome, {username}!")
        return redirect(next_url if next_url else "home")
    return render(request, 'users/register.html', {'next': next_url})

def login_view(request):
    next_url = request.GET.get("next", "/")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect(next_url or "home")
        messages.error(request, "Invalid username or password.")
    return render(request, "users/login.html", {"next": next_url})

def logout_view(request):
    logout(request)
    return redirect("/")


