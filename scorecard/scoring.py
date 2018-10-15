from django.db.models import Q
from .models import BusinessUnit, Product, ProductControl, ProductSecurityCapability, ProductSecurityRole, \
    SecurityCapability, SecurityRole, Status


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


def get_product_scores(product):

    # Calculate People score.
    people_score = 0
    security_roles = SecurityRole.objects.all()
    max_people_score = len(security_roles) # 1 point for each security role.
    prod_sec_roles = ProductSecurityRole.objects.filter(product=product)
    for security_role in security_roles:
        for prod_sec_role in prod_sec_roles:
            if prod_sec_role.role == security_role and prod_sec_role.person is not None:
                people_score += 1
                break

    # Calculate Process score.
    process_score = 0
    max_process_score = 1

    # Calculate Technology score.
    technology_score = 0
    security_capabilities = SecurityCapability.objects.all()
    product_security_capabilities = ProductSecurityCapability.objects.filter(Q(product=product) & ~Q(status__value=-1))
    max_technology_score = len(security_capabilities) * get_max_status_value()
    for product_security_capability in product_security_capabilities:
        technology_score += product_security_capability.status.value

    # Calculate Compliance score.
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
            print(f">>>> ERROR: Unknown product control status: '{product_control.status}'")

    return {'people_score':         people_score,
            'max_people_score':     max_people_score,
            'process_score':        process_score,
            'max_process_score':    max_process_score,
            'technology_score':     technology_score,
            'max_technology_score': max_technology_score,
            'compliance_score':     compliance_score,
            'max_compliance_score': max_compliance_score}


def update_all_product_scores():
    products = Product.objects.all()
    for product in products:
        update_product_score(product)


def update_product_score(product):
    scores = get_product_scores(product)
    product.people_score = scores['people_score']
    product.max_people_score = scores['max_people_score']
    product.people_percent_score = round(product.people_score * 100 / product.max_people_score, 1)
    product.process_score = scores['process_score']
    product.max_process_score = scores['max_process_score']
    product.process_percent_score = round(product.process_score * 100 / product.max_process_score, 1)
    product.technology_score = scores['technology_score']
    product.max_technology_score = scores['max_technology_score']
    product.technology_percent_score = round(product.technology_score * 100 / product.max_technology_score, 1)
    product.compliance_score = scores['compliance_score']
    product.max_compliance_score = scores['max_compliance_score']
    product.compliance_percent_score = round(product.compliance_score * 100 / product.max_compliance_score, 1)
    product.total_score = product.people_score + product.process_score + product.technology_score + \
        product.compliance_score
    product.max_total_score = product.max_people_score + product.max_process_score + product.max_technology_score + \
        product.max_compliance_score
    product.total_percent_score = round(product.total_score * 100 / product.max_total_score, 1)
    product.save()


def update_business_unit_scores():
    business_units = BusinessUnit.objects.all()
    for business_unit in business_units:
        score = 0
        max_score = 0
        products = Product.objects.filter(business_unit=business_unit)
        for product in products:
            score += product.total_score
            max_score += product.max_total_score
        percent_score = round(score * 100 / max_score, 1)
        business_unit.score = score
        business_unit.max_score = max_score
        business_unit.percent_score = percent_score
        business_unit.save()


def get_max_status_value():
    statuses = Status.objects.all()
    max_value = 0
    for status in statuses:
        if status.value > max_value:
            max_value = status.value
    return max_value

