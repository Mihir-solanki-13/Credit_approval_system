# customer/models.py
from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.BigIntegerField()
    monthly_income = models.BigIntegerField()
    phone_number = models.BigIntegerField()
    approved_limit = models.BigIntegerField()
    
    
