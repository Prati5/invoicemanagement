from django.test import TestCase
from .models import Invoice,Transaction
from decimal import Decimal

class InvoiceTestCase(TestCase):
    def setUp(self):
        data= {"customer": "test",
               "transactions": [
                    {
                    "product": "test prod",
                    "quantity": "1",
                    "price": "10.00"
                    }
                ]
            }

        validated_data = {
            "customer": data['customer'],
            "total_amount":0,
            "total_quantity": 0
        }   
        for transaction in data['transactions']:
            transaction['line_total'] = Decimal(transaction['price']) * Decimal(transaction["quantity"])
            validated_data['total_amount'] = validated_data['total_amount'] + int(transaction['line_total'])
            validated_data['total_quantity'] = validated_data['total_quantity'] + int(transaction['quantity'])
        invoice_instance = Invoice.objects.create(**validated_data)

        for transaction in data['transactions']:
            transaction['line_total'] = Decimal(transaction['price']) * Decimal(transaction["quantity"])
            transaction['invoice_id'] = invoice_instance
            Transaction.objects.create(**transaction)

    def tearDown(self) -> None:
        return super().tearDown()

    def get_invoice(self):
        invoice = Invoice.objects.get(id=1)
        self.assertEqual(invoice.customer, 'test')
        