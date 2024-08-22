from django.db import models

class OCRResult(models.Model):
    image = models.ImageField(upload_to='ocr/images')
    extracted_text = models.TextField()
    id_reservar = models.CharField(max_length=100, blank=True, null=True)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    monto = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OCR Result {self.id_reservar} from {self.uploaded_at}"
