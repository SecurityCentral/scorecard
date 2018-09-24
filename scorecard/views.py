from django.db import models
from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, ProductControl


def controls(request):
    product = Product.objects.get(id=request.GET.get("product"))
    control_list = ProductControl.objects.filter(product=product)
    return render(request, 'scorecard/controls.html', {'product': product, 'control_list': control_list})


def health(request):
    return HttpResponse(status=200)


def products(request):
    product_list = Product.objects.all()
    return render(request, 'scorecard/products.html', {'product_list': product_list})
