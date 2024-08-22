from django import forms
from.models import OCRResult

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = OCRResult
        fields = ['image']
