from django.db.models import Q
from .models import BusinessUnit, BUScore, Product, ProductControl, ProductSecurityCapability, ProductSecurityRole, \
    ProductScore, SecurityCapability, SecurityRole, Status

'''
    Executes all scoring related functionality.

    potential statuses:
          Implemented, complete   (green)     3
          partial                 (yellow)    2
          planned                 (orange)    1
          none, unknown           (red)       0
          not applicable          (grey)      -    
'''


def get_control_status_values():
    return {'Implemented': 3, 'complete': 3, 'partial': 2, 'planned': 1, 'none': 0, 'unknown': 0}


def calculate_process_score(product):

    process_score = 0
    security_roles = SecurityRole.objects.all()
    max_process_score = len(security_roles)  # 1 point for each security role.
    prod_sec_roles = ProductSecurityRole.objects.filter(product=product)
    for security_role in security_roles:
        for prod_sec_role in prod_sec_roles:
            if prod_sec_role.role == security_role and prod_sec_role.person is not None:
                process_score += 1
                break

    return process_score, max_process_score


def calculate_technology_score(product):

    technology_score = 0
    security_capabilities = SecurityCapability.objects.all()
    product_security_capabilities = ProductSecurityCapability.objects.filter(Q(product=product) & ~Q(status__value=-1))
    max_technology_score = len(security_capabilities) * get_max_status_value()
    for product_security_capability in product_security_capabilities:
        technology_score += product_security_capability.status.value

    return technology_score, max_technology_score


def calculate_compliance_score(product):

    compliance_score = 0
    status_values = get_control_status_values()
    # Get the product controls, but filter out all those with a status of 'not applicable'.
    product_controls = ProductControl.objects.filter(Q(product=product) & ~Q(status='not applicable')).\
        order_by('control__name')
    # max_compliance_score = len(product_controls) * 3  # A maximum possible score is 3 x the number of controls.
    max_compliance_score = 1
    for product_control in product_controls:
        try:
            compliance_score += status_values[product_control.status]
        except KeyError:
            print(">>>> ERROR: Unknown product control status: '%s'" % product_control.status)

    return compliance_score, max_compliance_score


def update_product_score(product):

    categories = ['process', 'technology', 'compliance']

    total_score = 0
    total_max_score = 0

    for category in categories:
        score = 0
        max_score = 1
        if category is 'process':
            score, max_score = calculate_process_score(product)
        if category is 'technology':
            score, max_score = calculate_technology_score(product)
        if category is 'compliance':
            score, max_score = calculate_compliance_score(product)
        total_score += score
        total_max_score += max_score
        prod_score, _ = ProductScore.objects.get_or_create(product=product, category=category)
        prod_score.score = score
        prod_score.max_score = max_score
        prod_score.save()

    prod_score, _ = ProductScore.objects.get_or_create(product=product, category='total')
    prod_score.score = total_score
    prod_score.max_score = total_max_score
    prod_score.save()


def update_all_product_scores():
    products = Product.objects.all()
    for product in products:
        update_product_score(product)


def update_business_unit_scores():
    business_units = BusinessUnit.objects.all()
    for business_unit in business_units:
        bu_score, _ = BUScore.objects.get_or_create(bu=business_unit)
        score = 0
        max_score = 0
        prod_scores = ProductScore.objects.filter(product__business_unit=business_unit, category='total')
        for prod_score in prod_scores:
            score += prod_score.score
            max_score += prod_score.max_score
        bu_score.score = score
        bu_score.max_score = max_score
        bu_score.save()


def get_max_status_value():
    statuses = Status.objects.all()
    max_value = 0
    for status in statuses:
        if status.value > max_value:
            max_value = status.value
    return max_value

