# loan/models.py
from django.db import models
from customer.models import Customer

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_amount = models.FloatField()
    interest_rate = models.FloatField()
    tenure = models.IntegerField()
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()

    def calculate_monthly_repayment(self):
        # Implement your logic for calculating monthly repayment (EMI)
        pass
