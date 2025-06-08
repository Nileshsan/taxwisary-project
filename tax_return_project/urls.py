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
from tax_return_project.views import home, base_view  # Import specific views if needed
from django.contrib.auth import views as auth_views

# Define a unified home view (or use tax_return_project.views.home if that fits your needs)
def home_view(request):
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home page
    path('', home_view, name='home'),
    
    # Include users app URLs with namespace
    path('users/', include('users.urls', namespace='users')),
    
    # Other specific views
    path('base/', base_view, name='base'),
    
    # Auth-related routes
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    # Include regime app URLs with its namespace
    path('regime/', include(('regime.urls', 'regime'), namespace='regime')),
    
    # Social and allauth URLs
    path('auth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
    
    # Password reset routes
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



