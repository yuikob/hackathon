from django.urls import path
from . import views

from django.shortcuts import render
from django.views.generic import TemplateView

urlpatterns = [
    path('pochi', TemplateView.as_view(template_name='pochi.html'), name="pochi"),
]