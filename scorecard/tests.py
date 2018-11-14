from django.test import TestCase
from scorecard import models, scoring

TEST_BUSINESS_UNIT_GROUP_NAME = "Test Business Group"
TEST_BUSINESS_UNIT_NAME = "Test Business Unit"
TEST_PRODUCT_NAME = "Test Product"


def setup_data():
    bu_group = models.BusinessUnitGroup.objects.create(name=TEST_BUSINESS_UNIT_GROUP_NAME, pp_id=1)
    bu = models.BusinessUnit.objects.create(name=TEST_BUSINESS_UNIT_NAME, bu_group=bu_group, pp_id=1)
    models.Product.objects.create(name=TEST_PRODUCT_NAME, business_unit=bu, published=False, pp_id=1)


class ScoringTests(TestCase):

    def test_compliance_scoring(self):
        setup_data()
        scoring.calculate_all_product_scores()
        scoring.calculate_all_business_unit_scores()
        product = models.Product.objects.first()
