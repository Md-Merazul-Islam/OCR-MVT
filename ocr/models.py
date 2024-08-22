from django.db import models
from decimal import Decimal

class OCRResult(models.Model):
    image = models.ImageField(upload_to='ocr/images')
    extracted_text = models.TextField()
    id_reservar = models.CharField(max_length=100, blank=True, null=True)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gmail = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"OCR Result from {self.uploaded_at}"
