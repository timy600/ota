from django.db import models
from .utils import random_five
#from django.contrib.auth.models import User

class User(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    invoice_currency = models.CharField(max_length=200)

    def __str__(self):
        name = self.firstname + " " +self.lastname
        return name

    def get_basic_data(self):
        """Basic Data DTO."""
        response = {
            'id': self.id,
            'lastname': self.lastname,
            'firstname': self.firstname,
            'email': self.email,
            'company': self.company
        }
        return response


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

    def get_basic_data(self):
        """Basic Data DTO."""
        response = {
            'id': self.id,
            'ref': self.ref,
            'date': self.date,
            'amount': self.amount
        }
        return response