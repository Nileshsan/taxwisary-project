"""
URL configuration for tax_return_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from tax_return_project.views import home, base_view  # Import specific views
from users import views as user_views  # Avoid conflicts with tax_return_project.views
from django.contrib.auth import views as auth_views

def home_view(request):
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Define only one root URL pattern to avoid conflicts
    path('', home_view, name='home'),

    # Include the users app URLs
    path('users/', include('users.urls')),
    # Other specific views
    path('base/', base_view, name='base'),

    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path('regime/', include(('regime.urls', 'regime'), namespace='regime')),

    path('auth/', include('social_django.urls', namespace='social')),

    path('accounts/', include('allauth.urls')),  
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    

    
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

