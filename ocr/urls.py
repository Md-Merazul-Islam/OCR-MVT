from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_and_extract, name='upload_and_extract'),
    path('confirm/<int:pk>/', views.ocr_confirm_view, name='ocr_confirm'),
    path('success/', views.success_view, name='success_page'),
]
