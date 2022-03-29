from django.urls import path
from . import views
from pochi.views import TestView

from django.shortcuts import render
from django.views.generic import TemplateView

urlpatterns = [
    path('pochi1', TemplateView.as_view(template_name='pochi1.html'), name="pochi1"),
    path('pochi2', TemplateView.as_view(template_name='pochi2.html'), name="pochi2"),
    path('pochi3', TemplateView.as_view(template_name='pochi3.html'), name="pochi3"),

    path('test', TestView.as_view(), name="test"),
]