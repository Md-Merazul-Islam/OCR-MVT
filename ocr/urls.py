from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_and_extract, name='upload_and_extract'),
]
