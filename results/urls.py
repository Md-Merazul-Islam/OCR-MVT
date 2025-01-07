
from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('search/', views.search_result, name='search'),
]
