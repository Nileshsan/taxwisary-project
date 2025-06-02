from django import forms
from .models import UserDocument

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UserDocument
        fields = ['file_name', 'file_type', 'file']
