from .models import Loan
from datetime import datetime
from django.utils import timezone

def past_loan_completed_on_time(customer):
    loans = Loan.objects.filter(customer__id=customer.id)
    loan_approved_volume=0
    total_loan_taken =0
    loans_in_current_year =0
    total_loan = 0
    paid_on_time = 0
    loan_approved_volume=0
    sum_of_current_loan =0
    if not loans.exists():
       return 100,loan_approved_volume,total_loan_taken,loans_in_current_year,sum_of_current_loan
    
    # find today's date and check each loan if completed  then check with tenure
    
    current_year = datetime.now().year
    curr_date = timezone.now().date()
    loans_in_current_year = loans.filter(start_date__year=current_year).count()
    

    for loan in loans:
        total_loan_taken+=1
        sum_of_current_loan = loan.tenure- loan.emis_paid_on_time
        loan_approved_volume+=loan.loan_amount
        if loan.end_date < curr_date:
            total_loan += 1
            if loan.emis_paid_on_time == loan.tenure:
                paid_on_time += 1
        else:
            sum_of_current_loan+=loan.loan_amount
 

    # Calculate the percentage of loans paid on time
    if total_loan > 0:
        percentage_paid_on_time = (paid_on_time / total_loan) * 100
    else:
        percentage_paid_on_time = 0
    
    if total_loan ==0:
        return 100,loan_approved_volume,total_loan_taken,loans_in_current_year,sum_of_current_loan
    return percentage_paid_on_time,loan_approved_volume,total_loan_taken,loans_in_current_year,sum_of_current_loan

        


def check_loan_eligibility(customer, loan_amount, interest_rate, tenure):
    percentage_paid_on_time,loan_approved_volume,total_loan_taken,loans_in_current_year,sum_current_emis = past_loan_completed_on_time(customer)
    weight_percentage_paid_on_time = 0.4
    weight_loan_approved_volume = 0.2  # Inversely proportional
    weight_total_loan_taken = 0.2  # Inversely proportional
    weight_loans_in_current_year = 0.2  # Inversely proportional

    # Define the maximum expected values for inversely proportional parameters
    max_loan_approved_volume = 100000  # Replace with the actual maximum value
    max_total_loan_taken = 50  # Replace with the actual maximum value
    max_loans_in_current_year = 12  # Replace with the actual maximum value

    # Normalize the values to be between 0 and 1
    normalized_percentage_paid_on_time = percentage_paid_on_time / 100
    normalized_loan_approved_volume = 1 - (loan_approved_volume / max_loan_approved_volume)
    normalized_total_loan_taken = 1 - (total_loan_taken / max_total_loan_taken)
    normalized_loans_in_current_year = 1 - (loans_in_current_year / max_loans_in_current_year)

    # Calculate the weighted sum of normalized values
    weighted_sum = (
        weight_percentage_paid_on_time * normalized_percentage_paid_on_time +
        weight_loan_approved_volume * normalized_loan_approved_volume +
        weight_total_loan_taken * normalized_total_loan_taken +
        weight_loans_in_current_year * normalized_loans_in_current_year
    )

    # Map the weighted sum to the credit rating scale (0 to 100)
    credit_rating = int(weighted_sum * 100)

    # Ensure credit rating is within the valid range (0 to 100)
    credit_rating = max(0, min(100, credit_rating))
    # print('credit_rating',credit_rating)

     
    # sum_current_emis = customer.current_debt
    monthly_salary = customer.monthly_income
    # print('credit_rating',credit_rating)
    # Implement credit approval logic
    if credit_rating > 50:
        approval = True
        corrected_interest_rate = interest_rate
    elif 50 > credit_rating > 30:
        if interest_rate > 12:
            approval = True
            corrected_interest_rate = interest_rate
        else:
            approval = False
            corrected_interest_rate = 12
    elif 30 > credit_rating > 10:
        if interest_rate > 16:
            approval = True
            corrected_interest_rate = interest_rate
        else:
            approval = False
            corrected_interest_rate = 16
    else:
        approval = False
        corrected_interest_rate = 0  # No loan approved if credit rating is less than 10

    # Additional checks
    if sum_current_emis > 0.5 * monthly_salary:
        approval = False
        corrected_interest_rate = 0  # Reset interest rate if total EMIs exceed 50% of monthly salary

    # print('arrp',approval)
    return approval, corrected_interest_rate

 