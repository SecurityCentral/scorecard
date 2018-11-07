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


def calculate_process_score(product):

    process_score = 0
    security_roles = models.SecurityRole.objects.all()
    security_capabilities = models.SecurityCapability.objects.filter(category__name=PROCESS)
    product_security_capabilities = models.ProductSecurityCapability.objects.\
        filter(Q(product=product) & Q(security_capability__category__name=PROCESS) & ~Q(status__value=-1))
    max_process_score = len(security_roles) + len(security_capabilities) * get_max_status_value()

    prod_sec_roles = models.ProductSecurityRole.objects.filter(product=product)
    for security_role in security_roles:
        for prod_sec_role in prod_sec_roles:
            if prod_sec_role.role == security_role and prod_sec_role.person is not None:
                process_score += 1
                break

    for product_security_capability in product_security_capabilities:
        process_score += product_security_capability.status.value

    return process_score, max_process_score


def calculate_technology_score(product):

    technology_score = 0
    security_capabilities = models.SecurityCapability.objects.filter(category__name=TECHNOLOGY)
    product_security_capabilities = models.ProductSecurityCapability.objects.\
        filter(Q(product=product) & Q(security_capability__category__name=TECHNOLOGY) & ~Q(status__value=-1))
    max_technology_score = len(security_capabilities) * get_max_status_value()

    for product_security_capability in product_security_capabilities:
        technology_score += product_security_capability.status.value

    return technology_score, max_technology_score


def calculate_compliance_score(product):

    compliance_score = 0
    security_capabilities = models.SecurityCapability.objects.filter(category__name=COMPLIANCE)
    product_security_capabilities = models.ProductSecurityCapability.objects.\
        filter(Q(product=product) & Q(security_capability__category__name=COMPLIANCE) & ~Q(status__value=-1))
    max_compliance_score = len(security_capabilities) * get_max_status_value()

    for product_security_capability in product_security_capabilities:
        compliance_score += product_security_capability.status.value

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

    return compliance_score, max_compliance_score


def calculate_product_score(product_id):

    product = models.Product.objects.get(id=product_id)
    categories = models.SecurityCategory.objects.all()

    total_score = 0
    total_max_score = 0

    for category in categories:
        score = 0
        max_score = 1
        if category.name == PROCESS:
            score, max_score = calculate_process_score(product)
        if category.name == TECHNOLOGY:
            score, max_score = calculate_technology_score(product)
        if category.name == COMPLIANCE:
            score, max_score = calculate_compliance_score(product)
        total_score += score
        total_max_score += max_score
        prod_score, _ = models.ProductScore.objects.update_or_create(product=product, category=category.name.lower(),
                                                                     defaults={'score': score, 'max_score': max_score})
    prod_score, _ = models.ProductScore.objects.update_or_create(product=product, category=TOTAL,
                                                                 defaults={'score': total_score,
                                                                           'max_score': total_max_score})


def calculate_all_product_scores():
    products = models.Product.objects.filter(published=True)
    for product in products:
        calculate_product_score(product.pk)


def calculate_business_unit_score(bu_id):
    score = 0
    max_score = 0
    prod_scores = models.ProductScore.objects.filter(product__business_unit=bu_id, category=TOTAL,
                                                     product__published=True)

    for prod_score in prod_scores:
        score += prod_score.score
        max_score += prod_score.max_score

    bu_score, _ = models.BUScore.objects.update_or_create(bu=bu_id, defaults={'score': score, 'max_score': max_score})


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
