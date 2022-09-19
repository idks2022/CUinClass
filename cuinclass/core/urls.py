from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', views.attendance, name='attendance'),
    path('fr-image/', views.fr_image, name='fr_image'),
    path('report/', views.report, name="report"),
    path('add/', views.add, name="add"), 
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)