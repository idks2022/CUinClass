from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', views.attendance, name='attendance'),
    path('fr-image/', views.fr_image, name='fr_image'),
    path("<int:id>", views.report, name="report"),
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)