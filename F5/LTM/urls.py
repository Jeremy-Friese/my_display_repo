from django.urls import path
from .views import BuildF5ConfigurationView

urlpatterns = [
    path('', BuildF5ConfigurationView.as_view(), name='validate-as3'),
]