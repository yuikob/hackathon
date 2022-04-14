from django.urls import path
from . import views
from pochi.views import UploadView, AnnotationView, get_pochi_info

from django.shortcuts import render
from django.views.generic import TemplateView

urlpatterns = [
    # path('pochi', TemplateView.as_view(template_name='pochi.html'), name="pochi"),
    # path('pochi2', TemplateView.as_view(template_name='pochi2.html'), name="pochi2"),
    # path('pochi3', TemplateView.as_view(template_name='pochi3.html'), name="pochi3"),

    path('upload', UploadView.as_view(), name="upload"),
    path('annotation', AnnotationView.as_view(), name="annotation"),
    path('info/', get_pochi_info, name="info"),
]