# from django import forms
# from .models import OCRResult

# class ImageUploadForm(forms.Form):
#     image = forms.ImageField()

# class OCRResultForm(forms.ModelForm):
#     class Meta:
#         model = OCRResult
#         fields = ['id_reservar', 'referencia', 'monto', 'name', 'phone', 'gmail']


#     def clean(self):
#             cleaned_data = super().clean()
#             id_reservar = cleaned_data.get('id_reservar')
#             referencia = cleaned_data.get('referencia')
#             monto = cleaned_data.get('monto')
#             name = cleaned_data.get('name')
#             phone = cleaned_data.get('phone')
#             gmail = cleaned_data.get('gmail')
            
#             if not (id_reservar and referencia and monto and name and phone and gmail):
#                 raise forms.ValidationError('All fields are required.')
            
#             return cleaned_data



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
