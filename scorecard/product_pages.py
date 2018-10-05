import requests
from scorecard.models import BusinessUnit, BusinessUnitGroup, Product


'''
    Acquires all business unit and product data via the Product Pages API.
'''

BUSINESS_UNIT_API = "https://pp.engineering.redhat.com/pp/api/latest/bugroups/"
PRODUCT_API = "https://pp.engineering.redhat.com/pp/api/latest/products/"


def update_product_data():

    # Get all the business unit data and create or update accordingly.

    business_unit_groups = requests.get(BUSINESS_UNIT_API, headers=dict(Accept="application/json"), verify=False).json()
    for bug in business_unit_groups:
        updated_bug, _ = BusinessUnitGroup.objects.get_or_create(pp_id=bug['id'])
        updated_bug.name = bug['name']
        updated_bug.save()
        business_units = bug['bus']
        for bu in business_units:
            updated_bu, _ = BusinessUnit.objects.get_or_create(pp_id=bu['id'])
            updated_bu.name = bu['name']
            updated_bu.bu_group = updated_bug
            updated_bu.save()

    # Get all the product data and create or update accordingly.

    products = requests.get(PRODUCT_API, headers=dict(Accept="application/json"), verify=False).json()

    for product in products:
        updated_product, _ = Product.objects.get_or_create(pp_id=product['id'])
        updated_product.name = product['name']
        updated_product.business_unit = BusinessUnit.objects.filter(pp_id=product['bu'])[0]
        updated_product.save()
