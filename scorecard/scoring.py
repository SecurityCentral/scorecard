from django.db.models import Q
from scorecard import models

'''
    Executes all scoring related functionality.

    potential statuses:
          Implemented, complete   (green)     3
          partial                 (yellow)    2
          planned                 (orange)    1
          none, unknown           (red)       0
          not applicable          (grey)      -    
'''

PROCESS = 'Process'
TECHNOLOGY = 'Technology'
COMPLIANCE = 'Compliance'
TOTAL = 'total'


def get_control_status_values():
    return {'Implemented': 3, 'complete': 3, 'partial': 2, 'planned': 1, 'none': 0, 'unknown': 0}


def calculate_category_score(product, category_name):

    process_score = 0
    items_supported = 0
    items_in_progress = 0
    security_capabilities = models.SecurityCapability.objects.filter(category__name=category_name)
    product_security_capabilities = models.ProductSecurityCapability.objects.\
        filter(Q(product=product) & Q(security_capability__category__name=category_name) & ~Q(status__value=-1))
    items_total = len(security_capabilities)

    for product_security_capability in product_security_capabilities:
        process_score += product_security_capability.status.value
        if product_security_capability.status.value is get_max_status_value():
            items_supported += 1
        if 0 < product_security_capability.status.value < get_max_status_value():
            items_in_progress += 1

    # Include security roles, if necessary.
    if category_name == PROCESS:
        security_roles = models.SecurityRole.objects.all()
        items_total += len(security_roles)

        prod_sec_roles = models.ProductSecurityRole.objects.filter(product=product)
        for security_role in security_roles:
            for prod_sec_role in prod_sec_roles:
                if prod_sec_role.role == security_role and prod_sec_role.person is not None:
                    process_score += get_max_status_value()
                    items_supported += 1
                    break

    max_process_score = items_total * get_max_status_value()

    print(">>>>>>>>>>>>>>>> max process score for %s: %d" % (category_name, max_process_score))

    return process_score, max_process_score, items_supported, items_in_progress, items_total


def calculate_compliance_score(product):

    compliance_score = 0
    items_supported = 0
    items_in_progress = 0
    security_capabilities = models.SecurityCapability.objects.filter(category__name=COMPLIANCE)
    product_security_capabilities = models.ProductSecurityCapability.objects.\
        filter(Q(product=product) & Q(security_capability__category__name=COMPLIANCE) & ~Q(status__value=-1))
    items_total = len(security_capabilities)
    max_compliance_score = items_total * get_max_status_value()

    for product_security_capability in product_security_capabilities:
        compliance_score += product_security_capability.status.value
        if product_security_capability.status.value is get_max_status_value():
            items_supported += 1
        if 0 < product_security_capability.status.value < get_max_status_value():
            items_in_progress += 1

    # compliance_score = 0
    # status_values = get_control_status_values()
    # # Get the product controls, but filter out all those with a status of 'not applicable'.
    # product_controls = ProductControl.objects.filter(Q(product=product) & ~Q(status='not applicable')).\
    #     order_by('control__name')
    # # max_compliance_score = len(product_controls) * 3  # A maximum possible score is 3 x the number of controls.
    # max_compliance_score = 1
    # for product_control in product_controls:
    #     try:
    #         compliance_score += status_values[product_control.status]
    #     except KeyError:
    #         print(">>>> ERROR: Unknown product control status: '%s'" % product_control.status)

    return compliance_score, max_compliance_score, items_supported, items_in_progress, items_total


def calculate_product_score(product_id):

    product = models.Product.objects.get(id=product_id)
    categories = models.SecurityCategory.objects.all()

    total_score = 0
    total_max_score = 0
    total_items_supported = 0
    total_items_in_progress = 0
    total_items_total = 0

    for category in categories:
        score, max_score, items_supported, items_in_progress, items_total = calculate_category_score(product,
                                                                                                     category.name)
        total_score += score
        total_max_score += max_score
        total_items_supported += items_supported
        total_items_in_progress += items_in_progress
        total_items_total += items_total
        prod_score, _ = models.ProductScore.objects.update_or_create(product=product, category=category.name.lower(),
                                                                     defaults={'score': score, 'max_score': max_score,
                                                                               'items_supported': items_supported,
                                                                               'items_in_progress': items_in_progress,
                                                                               'items_total': items_total})
    prod_score, _ = models.ProductScore.objects.update_or_create(product=product, category=TOTAL,
                                                                 defaults={'score': total_score,
                                                                           'max_score': total_max_score,
                                                                           'items_supported': total_items_supported,
                                                                           'items_in_progress': total_items_in_progress,
                                                                           'items_total': total_items_total})


def calculate_all_product_scores():
    products = models.Product.objects.filter(published=True)
    for product in products:
        calculate_product_score(product.pk)


def calculate_business_unit_score(bu_id):
    score = 0
    max_score = 0
    items_supported = 0
    items_in_progress = 0
    items_total = 0
    prod_scores = models.ProductScore.objects.filter(product__business_unit=bu_id, category=TOTAL,
                                                     product__published=True)

    # Total the constituent product scores.
    for prod_score in prod_scores:
        score += prod_score.score
        max_score += prod_score.max_score
        items_supported += prod_score.items_supported
        items_in_progress += prod_score.items_in_progress
        items_total += prod_score.items_total

    bu_score, _ = models.BUScore.objects.update_or_create(bu=bu_id, defaults={'score': score, 'max_score': max_score,
                                                                              'items_supported': items_supported,
                                                                              'items_in_progress': items_in_progress,
                                                                              'items_total': items_total})


def calculate_all_business_unit_scores():
    business_units = models.BusinessUnit.objects.all()
    for business_unit in business_units:
        calculate_business_unit_score(business_unit.pk)


def get_max_status_value():
    statuses = models.Status.objects.all()
    max_value = 0
    for status in statuses:
        if status.value > max_value:
            max_value = status.value
    return max_value
