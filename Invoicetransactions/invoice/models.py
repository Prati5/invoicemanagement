from django.db import models


class Invoice(models.Model):
    customer = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now=True)
    total_quantity= models.IntegerField()
    total_amount= models.IntegerField()


class Transaction(models.Model):
    product = models.CharField(max_length=500)
    quantity= models.IntegerField(default=0)
    price= models.DecimalField(max_digits=15, decimal_places=2)
    line_total=models.DecimalField(max_digits=15, decimal_places=2)
    invoice_id=models.ForeignKey(Invoice,related_name='invoice_transaction', on_delete=models.CASCADE)