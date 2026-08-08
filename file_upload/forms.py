from django import forms
from .models import UploadedFile

class UploadForm(forms.Form):
    file = forms.FileField(
        label = "Select a pdf",
        widget=forms.ClearableFileInput(attrs={
            'class' : 'upload-input',
                            })
    )