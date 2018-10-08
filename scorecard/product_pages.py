import requests
from scorecard.models import BusinessUnit, BusinessUnitGroup, Person, Product, ProductRole


'''
    Acquires all business unit and product data via the Product Pages API.
'''

PRODUCT_PAGES_API = 'https://pp.engineering.redhat.com/pp/api/latest'
BUSINESS_UNITS_API = PRODUCT_PAGES_API + '/bugroups/'
PRODUCTS_API = PRODUCT_PAGES_API + '/products/'
SECURITY_CHAMPION = "Security Escalation Contact"
PROGRAM_MANAGER = "Program Manager"
PRODUCT_SECURITY = "Product Security"


def update_product_data():

    # Get all the business unit data and create or update accordingly.

    bu_groups = requests.get(BUSINESS_UNITS_API, headers=dict(Accept='application/json'), verify=False).json()
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

    products = requests.get(PRODUCTS_API, headers=dict(Accept='application/json'), verify=False).json()

    for product in products:
        updated_product, _ = Product.objects.get_or_create(pp_id=product['id'])
        updated_product.name = product['name']
        updated_product.business_unit = BusinessUnit.objects.filter(pp_id=product['bu'])[0]
        updated_product.save()

        # For each product, get all the associated people.

        people = requests.get(PRODUCTS_API + str(updated_product.pp_id) + '/people/',
                              headers=dict(Accept='application/json'), verify=False).json()
        for person in people:
            product_role = ''
            if 'description__name' in person.keys():
                description = person['description__name']

                # Establish a Security Champion for the product.
                if SECURITY_CHAMPION.lower() in description.lower():
                    product_role = SECURITY_CHAMPION

                if "function__name" in person.keys():
                    function_name = person['function__name']

                    # Establish a Product Security Program Manager
                    if PROGRAM_MANAGER.lower() in description.lower() and PRODUCT_SECURITY.lower() in \
                            function_name.lower():
                        product_role = "Product Security Program Manager"

                if not product_role == "":
                    updated_person, _ = Person.objects.get_or_create(pp_id=person['id'])
                    updated_person.full_name = person['user_full_name']
                    updated_person.email = person['user_email']
                    updated_person.username = person['username']
                    updated_person.save()
                    product_role, _ = ProductRole.objects.get_or_create(description=product_role,
                                                                        product=updated_product, person=updated_person)
