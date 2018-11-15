import requests
from scorecard import models, scoring, set_up_data

'''
    Acquires all business unit and product data via the Product Pages API.
'''

PRODUCT_PAGES_API = 'https://pp.engineering.redhat.com/pp/api/latest/'
BUSINESS_UNITS_API = PRODUCT_PAGES_API + 'bugroups/'
PEOPLE_PARTIAL_API = '/people/?fields=id,description__name,function__name,user_full_name,user_email,username'
PRODUCTS_API = PRODUCT_PAGES_API + 'products/?fields=id,bu,name'
SECURITY_CHAMPION = "Security Escalation Contact"
PROGRAM_MANAGER = "Program Manager"
PRODUCT_SECURITY = "Product Security"
PRODUCT_SECURITY_PROGRAM_MANAGER = PRODUCT_SECURITY + " " + PROGRAM_MANAGER
# TRUSTED_CAS = '/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt'
TRUSTED_CAS = './scorecard/static/scorecard/ca-bundle.trust.crt'


def update_product_data():

    # Make sure all the base data is present (security capabilities, statuses, etc.)
    set_up_data.set_up_data()

    # Get all the business unit data and create or update accordingly.
    bu_groups = requests.get(BUSINESS_UNITS_API, headers=dict(Accept='application/json'), verify=TRUSTED_CAS).json()
    for bu_group in bu_groups:
        updated_bu_group, _ = models.BusinessUnitGroup.objects.update_or_create(
            pp_id=bu_group['id'], defaults={'name': bu_group['name']})
        business_units = bu_group['bus']
        for bu in business_units:
            updated_bu, _ = models.BusinessUnit.objects.update_or_create(
                pp_id=bu['id'], defaults={'name': bu['name'], 'bu_group': updated_bu_group})

    # Get all the product data and create or update accordingly.
    products = requests.get(PRODUCTS_API, headers=dict(Accept='application/json'), verify=TRUSTED_CAS).json()
    security_capabilities = models.SecurityCapability.objects.all()
    none_status = models.Status.objects.get(value=0)

    for product in products:
        updated_product, _ = models.Product.objects.update_or_create(
            pp_id=product['id'],
            defaults={'name': product['name'],
                      'business_unit': models.BusinessUnit.objects.filter(pp_id=product['bu'])[0]})

        # For each product, get all the associated people.
        people = requests.get(PRODUCT_PAGES_API + 'products/' + str(updated_product.pp_id) + PEOPLE_PARTIAL_API,
                              headers=dict(Accept='application/json'), verify=TRUSTED_CAS).json()

        security_roles = models.SecurityRole.objects.all()

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
                    updated_person, _ = models.Person.objects.update_or_create(
                        pp_id=person['id'],
                        defaults={'full_name': person['user_full_name'], 'email': person['user_email'],
                                  'username': person['username']})
                    product_role, _ = models.ProductSecurityRole.objects.get_or_create(
                        role=security_role, product=updated_product, person=updated_person)

                    # Since a person in the role was found, delete any previous "missing role" records.
                    models.ProductSecurityRole.objects.filter(
                        role=security_role, product=updated_product, person=None).delete()

            # If the product doesn't have a security role, report it and delete anyone previously listed in the role.
            if not role_found:
                models.ProductSecurityRole.objects.filter(role=security_role, product=updated_product).delete()
                product_role, _ = models.ProductSecurityRole.objects.get_or_create(
                    role=security_role, product=updated_product, person=None)

        # Update (or create default) security capabilities.
        for security_capability in security_capabilities:
            updated_security_capability_product, created = models.ProductSecurityCapability.objects.get_or_create(
                product=updated_product, security_capability=security_capability)
            if created:
                updated_security_capability_product.status = none_status
                updated_security_capability_product.save()

        scoring.calculate_product_score(updated_product.pk)

    scoring.calculate_all_business_unit_scores()
