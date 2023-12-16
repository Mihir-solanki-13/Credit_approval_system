# customer/models.py
from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    monthly_income = models.IntegerField()
    phone_number = models.IntegerField(max_length=15)  # Assuming phone numbers as strings
    approved_limit = models.IntegerField()
    current_debt = models.FloatField(default=0.0)
    
