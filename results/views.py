from django.shortcuts import render, redirect
from .forms import PDFUploadForm
from .models import StudentResult
from .utils import parse_pdf

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            try:
                results = parse_pdf(pdf_file)  # Parse the uploaded PDF

                for result in results:
                    StudentResult.objects.update_or_create(
                        roll_number=result['roll_number'],
                        defaults={
                            'gpa': result['gpa'],
                            'is_passed': result['is_passed'],
                            'failed_subjects': result['failed_subjects']
                        }
                    )
                return redirect('results:search')  # Redirect to search view after processing
            except Exception as e:
                # Handle parsing or database errors
                return render(request, 'upload_pdf.html', {
                    'form': form,
                    'error': f"An error occurred: {str(e)}"
                })
    else:
        form = PDFUploadForm()

    return render(request, 'upload_pdf.html', {'form': form})


def search_result(request):
    roll_number = request.GET.get('roll_number')
    result = None
    if roll_number:
        result = StudentResult.objects.filter(roll_number=roll_number).first()
    return render(request, 'search_result.html', {'result': result})
