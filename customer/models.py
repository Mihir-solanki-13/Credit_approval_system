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
    credit_score = models.IntegerField(default=0)

    def calculate_credit_score(self):
        # Implement logic to calculate credit score based on the provided criteria
        past_loans_paid_on_time = 0  # Retrieve this information from past loan data
        num_loans_taken = 0  # Retrieve this information from past loan data
        loan_activity_current_year = 0  # Retrieve this information from past loan data
        loan_approved_volume = 0  # Retrieve this information from past loan data
        sum_current_loans = 0  # Calculate the sum of current loans for the customer

        # Calculate credit score based on the provided criteria
        if sum_current_loans > self.approved_limit:
            self.credit_score = 0
        else:
            self.credit_score = (
                past_loans_paid_on_time * 10 +
                num_loans_taken * 5 +
                loan_activity_current_year * 7 +
                loan_approved_volume * 8
            )

    def calculate_approved_limit(self):
        # Implement logic to calculate approved limit based on salary
        self.approved_limit = round(36 * (self.monthly_income / 100000) * 100000)  # Round to nearest lakh
