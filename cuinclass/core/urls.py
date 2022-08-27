from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import *

urlpatterns = [
    path('', views.attendance, name='attendance'),
    path('image_upload/', views.attendance, name = 'image_upload'),
    # path('success/', views.uploadok, name = 'success'),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)