from django.shortcuts import render

def home(request):
    return render(request, 'index.html')


def About(request):
    return render(request, 'about.html')
