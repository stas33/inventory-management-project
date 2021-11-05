from django.test import TestCase
from .models import Company
# Create your tests here.

class CompanyTestCase(TestCase):

    def setUp(self):
        Company.objects.create(name='test1',
                               date_added=0,
                               address='test1',
                               postcode=0,
                               is_active=False)

    def test_company_exists(self):
        company_count = Company.objects.all().count()
        print(company_count)
        self.assertEqual(company_count, 1)
        self.assertNotEqual(company_count, 0)