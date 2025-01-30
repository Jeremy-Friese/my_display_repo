from django.urls import path
from . import views

urlpatterns = [
    path('calculate/', views.subnet_calculator, name='subnet_calculator'),
]