from django.contrib import admin
from .models import OCRResult

class OCRResultAdmin(admin.ModelAdmin):
    list_display = ('id_reservar', 'referencia', 'monto', 'name', 'phone', 'gmail', 'uploaded_at')
    search_fields = ('id_reservar', 'referencia', 'name', 'phone', 'gmail')
    list_filter = ('uploaded_at',)
    ordering = ('-uploaded_at',)  # Order by newest first

admin.site.register(OCRResult, OCRResultAdmin)
