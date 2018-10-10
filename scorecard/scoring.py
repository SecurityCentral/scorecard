from django.db.models import Q
from .models import Product, ProductControl


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


def get_product_score(product):
    status_values = get_control_status_values()
    # Get the product controls, but filter out all those with a status of 'not applicable'.
    product_controls = ProductControl.objects.filter(Q(product=product) & ~Q(status='not applicable')).\
        order_by('control__name')
    max_score = len(product_controls) * 3  # A maximum possible score is 3 x the number of controls.
    score = 0
    for product_control in product_controls:
        try:
            score += status_values[product_control.status]
        except KeyError:
            print(f">>>> ERROR: Unknown product control status: '{product_control.status}'")
    return score, max_score


def update_all_product_scores():
    products = Product.objects.all()
    for product in products:
        update_product_score(product)


def update_product_score(product):
    score, max_score = get_product_score(product)
    product.score = score
    product.max_score = max_score
    product.percent_score = round((score / max_score) * 100, 1)
    product.save()
