
from django.urls import path,include
from . import views
from .views import dashboard, login_view, logout_view, register,base_view
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import chatbot



urlpatterns = [
    path("", views.main_page, name="main_page"),
    path('', views.users_home, name='users-home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('users/logout/', logout_view, name='logout'),
    path("login/", auth_views.LoginView.as_view(), name="login"),

    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('base/', views.base_view, name='base'),  # Fixed name

    path('profile/', views.profile_view, name='profile'),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path("chatbot/", chatbot, name="chatbot"),  # Ensure this exists!
    path('regime/', views.regime_advisory, name='regime'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('password/change/', views.change_password, name='change_password'),
    path("about/", views.about_view, name="about"),
    path("upload-doc/", views.upload_doc, name="upload_doc"),
    path("regime-ai/", views.regime_ai_advice, name="regime_ai"),
    path("regime/", views.regime_page, name="regime_page"),
    path("upload-doc/", views.upload_doc, name="upload_doc"),
    path("regime-ai/", views.regime_ai_advice, name="regime_ai"),
    path("users/upload-doc/", views.upload_doc, name="upload_doc"),
    path("users/regime-ai/", views.regime_page, name="regime_ai"),


]


app_name = "users"
