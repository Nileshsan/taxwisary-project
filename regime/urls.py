from django.urls import path
from . import views

app_name = "regime"

urlpatterns = [
    path("", views.regime_advisory, name="advisory"),
    path('regime_ai/', views.regime_ai, name='regime_ai'),
    path('upload_doc/', views.upload_doc, name='upload_doc'),
    path("advisory/", views.regime_advisory, name="advisory"),





]

    