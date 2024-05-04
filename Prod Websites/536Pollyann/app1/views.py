import os
import sys
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
import subprocess
import re

# Create your views here.
def home(request):
    return render(request,"prime.html")

def pictures(request):
    return render(request,"pictures.html")

def ammenities(request):
    return render(request,"ammenities.html")

def location(request):
    return render(request,"location.html")

def sitemap(request):
    return render(request,"sitemap.xml")
