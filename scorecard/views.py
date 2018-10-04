from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render
from django.template.defaulttags import register
from .models import BusinessUnit, Product, ProductControl, SecurityCapabilityProduct
from scorecard import scoring


def businessunitsview(request):
    bu_list = BusinessUnit.objects.all().order_by('name')
    return render(request, 'scorecard/businessunits.html', {'bu_list': bu_list})


def controlsview(request):
    product = Product.objects.get(id=request.GET.get("product"))
    product_control_list = ProductControl.objects.filter(Q(product=product) & ~Q(status='not applicable')).\
        order_by('control__family__label', 'control__name')
    security_capability_product_list = SecurityCapabilityProduct.objects.filter(Q(product=product) &
        ~Q(status__name='not applicable')).order_by('security_capability__name')

    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)

    return render(request, 'scorecard/controls.html',
                  {'product': product,
                   'product_control_list': product_control_list,
                   'control_status_values': scoring.get_control_status_values(),
                   'security_capability_product_list': security_capability_product_list})


def health(request):
    return HttpResponse(status=200)


def productsview(request):
    # scoring.update_product_scores()
    business_unit = BusinessUnit.objects.get(id=request.GET.get("bu"))
    product_list = Product.objects.filter(Q(business_unit=business_unit))
    return render(request, 'scorecard/products.html', {'product_list': product_list, 'bu': business_unit})
