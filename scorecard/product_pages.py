import requests
from .models import BusinessUnit, BusinessUnitGroup, Person, Product, ProductSecurityCapability, ProductSecurityRole, \
    SecurityCapability, SecurityRole, Status
from scorecard import scoring

'''
    Acquires all business unit and product data via the Product Pages API.
'''

PRODUCT_PAGES_API = 'https://pp.engineering.redhat.com/pp/api/latest'
BUSINESS_UNITS_API = PRODUCT_PAGES_API + '/bugroups/'
PRODUCTS_API = PRODUCT_PAGES_API + '/products/'
SECURITY_CHAMPION = "Security Escalation Contact"
PROGRAM_MANAGER = "Program Manager"
PRODUCT_SECURITY = "Product Security"
PRODUCT_SECURITY_PROGRAM_MANAGER = PRODUCT_SECURITY + " " + PROGRAM_MANAGER
# TRUSTED_CAS = '/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt'
TRUSTED_CAS = './scorecard/static/scorecard/ca-bundle.trust.crt'


def update_product_data():

    # Get all the business unit data and create or update accordingly.

    bu_groups = requests.get(BUSINESS_UNITS_API, headers=dict(Accept='application/json'), verify=TRUSTED_CAS).json()
    for bu_group in bu_groups:
        updated_bu_group, _ = BusinessUnitGroup.objects.get_or_create(pp_id=bu_group['id'])
        updated_bu_group.name = bu_group['name']
        updated_bu_group.save()
        business_units = bu_group['bus']
        for bu in business_units:
            updated_bu, _ = BusinessUnit.objects.get_or_create(pp_id=bu['id'])
            updated_bu.name = bu['name']
            updated_bu.bu_group = updated_bu_group
            updated_bu.save()

    # Get all the product data and create or update accordingly.
    products = requests.get(PRODUCTS_API, headers=dict(Accept='application/json'), verify=TRUSTED_CAS).json()
    security_capabilities = SecurityCapability.objects.all()
    none_status = Status.objects.get(value=0)

    for product in products:
        updated_product, _ = Product.objects.get_or_create(pp_id=product['id'])
        updated_product.name = product['name']
        updated_product.business_unit = BusinessUnit.objects.filter(pp_id=product['bu'])[0]
        updated_product.save()

        # For each product, get all the associated people.
        people = requests.get(PRODUCTS_API + str(updated_product.pp_id) + '/people/',
                              headers=dict(Accept='application/json'), verify=TRUSTED_CAS).json()

        security_roles = SecurityRole.objects.all()

        for security_role in security_roles:
            role_found = False
            sec_role_desc = security_role.description.lower()
            sec_role_func = security_role.function.lower()
            for person in people:
                if 'description__name' in person.keys():
                    description_name = person['description__name'].lower()
                else:
                    description_name = ''
                if 'function__name' in person.keys():
                    function_name = person['function__name'].lower()
                else:
                    function_name = ''
                if ((sec_role_desc == description_name and
                     sec_role_func == function_name) or
                    (sec_role_desc == '' and
                     function_name == sec_role_func) or
                    (sec_role_desc == description_name and
                     sec_role_func == '')):
                    role_found = True

                    # Record the product role.
                    updated_person, _ = Person.objects.get_or_create(pp_id=person['id'])
                    updated_person.full_name = person['user_full_name']
                    updated_person.email = person['user_email']
                    updated_person.username = person['username']
                    updated_person.save()
                    product_role, _ = ProductSecurityRole.objects.get_or_create(role=security_role,
                                                                                product=updated_product,
                                                                                person=updated_person)

            # If the product doesn't have a security role, report it.
            if not role_found:
                product_role, _ = ProductSecurityRole.objects.get_or_create(role=security_role,
                                                                            product=updated_product, person=None)

        # Update (or create default) security capabilities.
        for security_capability in security_capabilities:
            updated_security_capability_product, created = ProductSecurityCapability.objects.get_or_create(
                product=updated_product, security_capability=security_capability)
            if created:
                updated_security_capability_product.status = none_status
                updated_security_capability_product.save()

        scoring.update_product_score(updated_product)
        scoring.update_business_unit_scores()
