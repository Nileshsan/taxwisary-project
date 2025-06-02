from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def users_home(request):
    return render(request, 'users/users_home.html')

def home(request):
    return render(request, 'users/home.html')  # Correct path

def home_view(request):
    return render(request, 'home.html')

def user_view(request):
    return render(request, 'user.html')  # Ensure it's a different template

def base_view(request):
    return render(request, 'users/base.html')  # Include 'users/' in the path

