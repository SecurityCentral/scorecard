from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

# Create your views here.
def health(request):
    return HttpResponse(status=200)
