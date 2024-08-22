from django.shortcuts import render
from .forms import ImageUploadForm
from .models import OCRResult
from PIL import Image
import pytesseract
import re

def upload_and_extract(request):
    result = None
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']
            image = Image.open(image_file)

            # Perform OCR
            extracted_text = pytesseract.image_to_string(image)

            # Extract the "ID RESERVAR"
            id_reservar_match = re.search(r'ID RESERVAR\s*(\w+)', extracted_text, re.IGNORECASE)
            id_reservar = id_reservar_match.group(1) if id_reservar_match else None

            # Extract the "REFERENCIA"
            referencia_match = re.search(r'REFERENCIA\s*(\d+)', extracted_text, re.IGNORECASE)
            referencia = referencia_match.group(1) if referencia_match else None

            # Extract the "MONTO"
            monto_match = re.search(r'MONTO\s*([\d,]+\.\d{2})', extracted_text, re.IGNORECASE)
            monto = monto_match.group(1) if monto_match else None

            # Save to the database
            result = OCRResult.objects.create(
                image=image_file,
                extracted_text=extracted_text,
                id_reservar=id_reservar,
                referencia=referencia,
                monto=monto
            )

    else:
        form = ImageUploadForm()

    return render(request, 'upload_and_extract.html', {'form': form, 'result': result})
