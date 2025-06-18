from django.urls import path
from . import views, auth_views, advisory_views, report_views
from django.contrib.auth.views import LogoutView
from .views import contact_view

app_name = "users"

urlpatterns = [
    # General Pages
    path("", views.main_page, name="main_page"),
    path("users-home/", views.users_home, name="users-home"),
    path("base/", views.base_view, name="base"),  # Used by your template's TAX_AI link.
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("password/change/", views.change_password, name="change_password"),
    path("chatbot/", views.chatbot, name="chatbot"),
    path("about/", views.about_view, name="about"),
    path("upload-doc/", views.upload_doc, name="upload_doc"),
    path("regime/", views.regime_page, name="regime_page"),
    
    # Authentication Routes
    path("register/", auth_views.register, name="register"),
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
    
    # Advisory (Tax Assistant) Routes
    path("advisory/personal/", advisory_views.advisory_personal, name="advisory_personal"),
    path("advisory/personal/confirm/", advisory_views.advisory_personal_confirm, name="advisory_personal_confirm"),
    path("advisory/income/", advisory_views.advisory_income, name="advisory_income"),
    path("advisory/income/confirm/", advisory_views.advisory_income_confirm, name="advisory_income_confirm"),
    path("advisory/deductions/", advisory_views.advisory_deductions, name="advisory_deductions"),
    path("advisory/summary/", advisory_views.advisory_summary, name="advisory_summary"),
    
    # Report Generation
    path("report/", report_views.generate_report, name="generate_report"),
    
    # Contact
    path('contact/', contact_view, name='contact'),
]





