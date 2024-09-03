from django.contrib import admin
from hello import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', views.admin_user),
    path('',include('home.home_urls')),
    
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)