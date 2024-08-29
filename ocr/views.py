from django.shortcuts import render, redirect
from .forms import ImageUploadForm, OCRResultForm
from .models import OCRResult
from PIL import Image
import pytesseract
import re
from decimal import Decimal
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect

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
            result.save()  

            return redirect('ocr_confirm', pk=result.pk)  

    else:
        form = ImageUploadForm()

    return render(request, 'upload_and_extract.html', {'form': form, 'ocr_result': result})


from django.shortcuts import render, redirect, get_object_or_404
from .models import OCRResult
from .forms import OCRResultForm

# def ocr_confirm_view(request, pk):
#     ocr_result = get_object_or_404(OCRResult, pk=pk)
#     form = OCRResultForm(instance=ocr_result)

#     if request.method == 'POST':
#         form = OCRResultForm(request.POST, instance=ocr_result)
#         if form.is_valid():
#             form.save()
#             return redirect('success_page')  
#         else:
#             # If form is invalid, return the form with error messages
#             error_message = form.errors.as_text()  # Get error messages as plain text
#             return render(request, 'ocr_confirm.html', {'form': form, 'ocr_result': ocr_result, 'error_message': error_message})

#     return render(request, 'ocr_confirm.html', {'form': form, 'ocr_result': ocr_result})


def success_view(request):
    return render(request, 'success.html')




def ocr_results_view(request):
    ocr_results = OCRResult.objects.all()
    total_amount = OCRResult.objects.aggregate(total_amount=Sum('monto'))['total_amount'] or Decimal('0.00')

    return render(request, 'ocr_results.html', {'ocr_results': ocr_results, 'total_amount': total_amount})



def edit_ocr_result_view(request, pk):
    ocr_result = get_object_or_404(OCRResult, pk=pk)
    
    if request.method == 'POST':
        form = OCRResultForm(request.POST, instance=ocr_result)
        if form.is_valid():
            form.save()
            return redirect('ocr_results')  
        else:
            print(form.errors)  # Print errors for debugging
    else:
        form = OCRResultForm(instance=ocr_result)
    
    return render(request, 'edit_ocr_result.html', {'form': form, 'ocr_result': ocr_result})





def delete_ocr_result(request, pk):
    ocr_result = get_object_or_404(OCRResult, pk=pk)
    if request.method == 'POST':
        ocr_result.delete()
        return redirect('ocr_results')
    return render(request, 'confirm_delete.html', {'ocr_result': ocr_result})



from django.shortcuts import render, redirect, get_object_or_404
from .models import OCRResult
from .forms import OCRResultForm
from .forms import ImageUploadForm, OCRResultForm

def ocr_confirm_view(request, pk):
    ocr_result = get_object_or_404(OCRResult, pk=pk)
    
    if request.method == 'POST':
        form = OCRResultForm(request.POST, instance=ocr_result)
        if form.is_valid():
            # Save only fields that are not None
            cleaned_data = form.cleaned_data
            if not cleaned_data.get('id_reservar'):
                cleaned_data['id_reservar'] = ''  # Set default value if None
            if not cleaned_data.get('referencia'):
                cleaned_data['referencia'] = ''
            if not cleaned_data.get('monto'):
                cleaned_data['monto'] = ''
            if not cleaned_data.get('name'):
                cleaned_data['name'] = ''
            if not cleaned_data.get('phone'):
                cleaned_data['phone'] = ''
            if not cleaned_data.get('gmail'):
                cleaned_data['gmail'] = ''
            
            form.save(commit=False)  # Commit changes to the database
            # Update the instance with the cleaned data
            for field, value in cleaned_data.items():
                setattr(ocr_result, field, value)
            ocr_result.save()
            
            return redirect('success_page')
        else:
            # If form is invalid, render the form with errors
            error_message = form.errors.as_text()
            return render(request, 'ocr_confirm.html', {'form': form, 'ocr_result': ocr_result, 'error_message': error_message})

    form = OCRResultForm(instance=ocr_result)
    return render(request, 'ocr_confirm.html', {'form': form, 'ocr_result': ocr_result})
