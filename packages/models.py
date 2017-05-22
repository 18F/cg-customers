from django.db import models
from djmoney.models.fields import MoneyField

class Package(models.Model):
    package_name = models.CharField(max_length=64)
    yearly_price = MoneyField(max_digits=12, decimal_places=2, default_currency='USD')
