from django.db import models
from invoice.models import Invoice

# Create your models here.

# class Transaction(models.Model):
#     product = models.CharField(max_length=500)
#     quantity= models.IntegerField(default=0)
#     price= models.DecimalField(max_digits=15, decimal_places=2)
#     line_total=models.DecimalField(max_digits=15, decimal_places=2)
#     invoice_id=models.ForeignKey(Invoice, on_delete=models.CASCADE)