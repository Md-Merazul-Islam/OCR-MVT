
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . views import home,About
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home_page'),
    path('about/', About, name='about_page'),
    path('ocr/',include('ocr.urls')),
    path('account/',include('account.urls')),
    
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)