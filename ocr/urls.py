from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_and_extract, name='upload_and_extract'),
    path('confirm/<int:pk>/', views.ocr_confirm_view, name='ocr_confirm'),
    path('success/', views.success_view, name='success_page'),
    path('results/', views.ocr_results_view, name='ocr_results'),
     path('edit/<int:pk>/', views.edit_ocr_result_view, name='edit_ocr_result'),
    path('delete/<int:pk>/', views.delete_ocr_result, name='delete_ocr_result'),
]
