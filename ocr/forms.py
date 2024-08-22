from django import forms
from .models import OCRResult

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class OCRResultForm(forms.ModelForm):
    class Meta:
        model = OCRResult
        fields = ['id_reservar', 'referencia', 'monto', 'name', 'phone', 'gmail']
