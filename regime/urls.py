from django.urls import path
from . import views

app_name = "regime"

urlpatterns = [
    path("", views.regime_advisory, name="advisory"),
    path('regime-ai/', views.regime_ai, name='regime_ai'),



]

    