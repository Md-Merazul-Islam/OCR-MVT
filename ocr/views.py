from django.shortcuts import render, redirect
from .forms import ImageUploadForm, OCRResultForm
from .models import OCRResult
from PIL import Image
import pytesseract
import re
from decimal import Decimal

def upload_and_extract(request):
    result = None  # Initialize result to None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']
            image = Image.open(image_file)

            # Perform OCR
            extracted_text = pytesseract.image_to_string(image)

            # Extract data
            id_reservar_match = re.search(r'ID RESERVAR\s*(\w+)', extracted_text, re.IGNORECASE)
            id_reservar = id_reservar_match.group(1) if id_reservar_match else None

            referencia_match = re.search(r'REFERENCIA\s*(\d+)', extracted_text, re.IGNORECASE)
            referencia = referencia_match.group(1) if referencia_match else None

            monto_match = re.search(r'MONTO\s*([\d,]+\.\d{2})', extracted_text, re.IGNORECASE)
            monto_str = monto_match.group(1) if monto_match else None

            if monto_str:
                monto_str = monto_str.replace(',', '')
                monto = Decimal(monto_str)
            else:
                monto = None

            # Create or update the result
            result = OCRResult(
                image=image_file, 
                extracted_text=extracted_text,  
                id_reservar=id_reservar,
                referencia=referencia,
                monto=monto
            )
            result.save()  # Save the result to get an ID

            return redirect('ocr_confirm', pk=result.pk)  # Redirect to confirmation page with the ID

    else:
        form = ImageUploadForm()

    return render(request, 'upload_and_extract.html', {'form': form, 'ocr_result': result})


from django.shortcuts import render, redirect, get_object_or_404
from .models import OCRResult
from .forms import OCRResultForm

def ocr_confirm_view(request, pk):
    ocr_result = get_object_or_404(OCRResult, pk=pk)
    form = OCRResultForm(instance=ocr_result)

    if request.method == 'POST':
        form = OCRResultForm(request.POST, instance=ocr_result)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page after saving

    return render(request, 'ocr_confirm.html', {'form': form, 'ocr_result': ocr_result})


def success_view(request):
    return render(request, 'success.html')
