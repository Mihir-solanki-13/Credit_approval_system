
def check_loan_eligibility(customer, loan_amount, interest_rate, tenure):
    return True,1
    # Retrieve customer data
    credit_rating = credit_rating()
    sum_current_emis = customer.current_debt
    monthly_salary = customer.monthly_income

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

   
    return approval, corrected_interest_rate

def credit_rating():
    return 100