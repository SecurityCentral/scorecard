from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render
from django.template.defaulttags import register
from .models import BusinessUnit, BUScore, Product, ProductControl, ProductScore, ProductSecurityRole, \
    ProductSecurityCapability
from scorecard import product_pages, scoring

NOT_APPLICABLE = "not applicable"


def businessunitsview(request):
    bu_group_set = set()
    bu_score_set = set()
    product_list = Product.objects.filter(published=True)
    all_bu_scores = BUScore.objects.all().order_by('bu__name')
    for product in product_list:
        bu_group_set.add(product.business_unit.bu_group)
        for bu_score in all_bu_scores:
            if product.business_unit == bu_score.bu:
                bu_score_set.add(bu_score)
    bu_group_list = list(bu_group_set)
    bu_score_list = list(bu_score_set)
    return render(request, 'scorecard/businessunits.html', {'bu_group_list': bu_group_list,
                                                            'bu_score_list': bu_score_list})


def proddetailsview(request):
    product_score = ProductScore.objects.get(product__id=request.GET.get('product'), category=scoring.TOTAL)
    proc = ProductScore.objects.get(product__id=request.GET.get('product'), category=scoring.PROCESS.lower())
    tech = ProductScore.objects.get(product__id=request.GET.get('product'), category=scoring.TECHNOLOGY.lower())
    comp = ProductScore.objects.get(product__id=request.GET.get('product'), category=scoring.COMPLIANCE.lower())
    proc_sub_categories_set = set()
    tech_sub_categories_set = set()
    comp_sub_categories_set = set()

    product_control_list = ProductControl.objects.\
        filter(Q(product=product_score.product) & ~Q(status=NOT_APPLICABLE)).\
        order_by('control__family__label', 'control__name')

    proc_list = ProductSecurityCapability.objects.\
        filter(Q(product=product_score.product) &
               Q(security_capability__category__name=scoring.PROCESS) & ~Q(status__name=NOT_APPLICABLE)).\
        order_by('security_capability__sub_category', 'security_capability__name')
    for proc_item in proc_list:
        proc_sub_categories_set.add(proc_item.security_capability.sub_category)
    proc_sub_categories_list = list(proc_sub_categories_set)

    tech_list = ProductSecurityCapability.objects.\
        filter(Q(product=product_score.product) &
               Q(security_capability__category__name=scoring.TECHNOLOGY) & ~Q(status__name=NOT_APPLICABLE)).\
        order_by('security_capability__sub_category', 'security_capability__name')
    for tech_item in tech_list:
        tech_sub_categories_set.add(tech_item.security_capability.sub_category)
    tech_sub_categories_list = list(tech_sub_categories_set)

    comp_list = ProductSecurityCapability.objects.\
        filter(Q(product=product_score.product) &
               Q(security_capability__category__name=scoring.COMPLIANCE) & ~Q(status__name=NOT_APPLICABLE)).\
        order_by('security_capability__sub_category', 'security_capability__name')
    for comp_item in comp_list:
        comp_sub_categories_set.add(comp_item.security_capability.sub_category)
    comp_sub_categories_list = list(comp_sub_categories_set)

    product_roles_list = ProductSecurityRole.objects.filter(Q(product=product_score.product)).\
        order_by('role__description')

    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)

    return render(request, 'scorecard/proddetails.html',
                  {'product_score': product_score,
                   'proc': proc,
                   'tech': tech,
                   'comp': comp,
                   'product_control_list': product_control_list,
                   'control_status_values': scoring.get_control_status_values(),
                   'proc_list': proc_list,
                   'tech_list': tech_list,
                   'comp_list': comp_list,
                   'proc_sub_categories_list': proc_sub_categories_list,
                   'tech_sub_categories_list': tech_sub_categories_list,
                   'comp_sub_categories_list': comp_sub_categories_list,
                   'product_roles_list': product_roles_list})


def health(request):
    return HttpResponse(status=200)


def productsview(request):
    business_unit = BusinessUnit.objects.get(id=request.GET.get('bu'))
    product_score_list = ProductScore.objects.filter(product__business_unit=business_unit, category=scoring.TOTAL,
                                                     product__published=True)
    return render(request, 'scorecard/products.html', {'product_score_list': product_score_list, 'bu': business_unit})


def submit(request):
    if 'update' in request.POST:
        product_pages.update_product_data()
    return businessunitsview(request)
