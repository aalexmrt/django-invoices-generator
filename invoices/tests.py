from django.test import TestCase
from invoices.models import Client, Invoice, Company
import datetime

class TestModels(TestCase):
    def setUp(self):
        client_test = Client.objects.create(name="Paco")
        company_test = Company.objects.create(name="Pescados Jose")
        Invoice.objects.create(number="hello-001", date="2022-12-12", mailed=1, client=client_test, company=company_test)

    def test_client_generation(self):
        client_test = Client.objects.get(name="Paco")
        self.assertEqual(client_test.name, "Paco")

    def test_company_generation(self):
        company_test = Company.objects.get(name="Pescados Jose")
        self.assertEqual(company_test.name, "Pescados Jose")

    def test_invoice_generation(self):
        invoice_test = Invoice.objects.get(number="hello-001")
        self.assertEqual(invoice_test.date, datetime.date(2022, 12, 12))
        self.assertEqual(invoice_test.mailed, 1)
        self.assertEqual(invoice_test.client.name, "Paco")
        self.assertEqual(invoice_test.company.name, "Pescados Jose")
