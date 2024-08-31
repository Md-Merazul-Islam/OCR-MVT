

from django import forms
from .models import OCRResult
from django import forms
from .models import OCRResult

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = OCRResult
        fields = ['image']

class OCRResultForm(forms.ModelForm):
    class Meta:
        model = OCRResult
        fields = ['id_reservar', 'referencia', 'monto', 'name', 'phone', 'gmail']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure all fields are required and set default values if None
        for field in self.fields:
            self.fields[field].required = True
            if self.instance and getattr(self.instance, field) is None:
                self.fields[field].initial = ''  # Set default initial value
    
    def clean(self):
        cleaned_data = super().clean()
        # Custom validation example: Ensure all required fields are filled
        for field in ['id_reservar', 'referencia', 'monto', 'name', 'phone', 'gmail']:
            if not cleaned_data.get(field):
                cleaned_data[field] = ''  # Set default value if None

        # Additional validation checks can be added here

        return cleaned_data
