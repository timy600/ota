"""
from crm.models import User, Invoice
u1 = User(name="Thibaut", email="test", company="Total", country="France", invoice_currency="euro")
u1.save()
i1 =Invoice(user=u1, amount=10, date="2022-01-01", status=True)
i1.save()
User.objects.all()
"""

from django.db import models
from .utils import random_five

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    invoice_currency = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref = models.CharField(max_length=9)
    amount = models.FloatField(default=0)
    date = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.ref

    def clean(self):
        prefix = "OTA-"
        number = random_five()
        ref = prefix + number
        self.ref = ref
