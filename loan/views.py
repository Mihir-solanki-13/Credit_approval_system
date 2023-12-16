# loan/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Loan
from .serializers import *
from customer.models import Customer
from .loan_eligibility import check_loan_eligibility
from datetime import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta  # Import relativedelta
from customer.serializers import CustomerSerializer


@api_view(['POST'])
def check_eligibility(request):
    if request.method == 'POST':
        serializer = CheckEligibilityRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Extract validated data
            data = serializer.validated_data

            # Fetch customer data from the database
            try:
                customer = Customer.objects.get(id=data['customer_id'])
            except Customer.DoesNotExist:
                return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

            # Implement your logic to check eligibility
            approval, corrected_interest_rate = check_loan_eligibility(customer, data['loan_amount'], data['interest_rate'], data['tenure'])
            monthly_installment = calculate_monthly_installment(data['loan_amount'], data['interest_rate'], data['tenure'])
            # Prepare the response data
            response_data = {
                'customer_id': data['customer_id'],
                'approval': approval,
                'interest_rate': data['interest_rate'],
                'corrected_interest_rate': corrected_interest_rate,
                'tenure': data['tenure'],
                'monthly_installment': monthly_installment,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def calculate_monthly_installment(loan_amount, interest_rate, tenure):
    # Convert annual interest rate to monthly and percentage to decimal
    r = (interest_rate / 12) / 100

    # Calculate total number of payments
    n = tenure

    # Calculate monthly installment using the formula
    emi = (loan_amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)

    return emi


@api_view(['POST'])
def create_loan(request):
    if request.method == 'POST':
        serializer = CreateLoanSerializer(data=request.data)
        try:
            if serializer.is_valid():
                data = serializer.validated_data
                customer_id = data['customer_id']

                # Fetch customer details from the database
                try:
                    customer = Customer.objects.get(pk=customer_id)
                except Customer.DoesNotExist:
                    return Response({'error': 'Customer not found.'}, status=status.HTTP_400_BAD_REQUEST)

                # Check eligibility and process the loan
                # print('mihir')
                approval, corrected_interest_rate  = check_loan_eligibility(customer, data['loan_amount'], data['interest_rate'], data['tenure'])
                # print('approval' ,approval)
                monthly_installment = calculate_monthly_installment(data['loan_amount'], data['interest_rate'], data['tenure'])
                print('monthly_installment' ,monthly_installment)
                if approval == False:
                    response_data = {
                    'loan_id': None,
                    'customer_id': customer.id,
                    'loan_approved': approval,
                    'message': 'Not approved',
                    'monthly_installment': monthly_installment,
                   }

                    return Response(response_data, status=status.HTTP_201_CREATED)
                

                start_date = timezone.now().date()

                new_loan = Loan.objects.create(
                    customer=customer,
                    loan_amount=data['loan_amount'],
                    interest_rate=data['interest_rate'],
                    tenure=data['tenure'],
                    emis_paid_on_time=0,  # Assuming no EMIs paid on time initially
                    start_date=start_date,
                    end_date=start_date + relativedelta(months=data['tenure']),  # Correct the months parameter
                )

                response_data = {
                    'loan_id': new_loan.id,
                    'customer_id': customer.id,
                    'loan_approved': approval,
                    'message': 'Loan approved',
                    'monthly_installment': monthly_installment,
                }

                return Response(response_data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.get(pk=loan_id)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize loan data
    loan_serializer = LoanSerializer(loan)

    # Serialize customer data
    customer_serializer = CustomerSerializer(loan.customer)
    monthly_installment = calculate_monthly_installment( loan.loan_amount, loan.interest_rate,loan.tenure)
    # Construct the response data
    response_data = {
        'loan_id': loan.id,
        'customer': customer_serializer.data,
        'loan_amount': loan.loan_amount,
        'interest_rate': loan.interest_rate,
        'monthly_installment': monthly_installment,  # Replace with your calculation logic
        'tenure': loan.tenure,
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_loans(request, customer_id):
    try:
        loans = Loan.objects.filter(customer__id=customer_id)
    except Loan.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
    print('loan',loans)
    # Serialize each loan data
    loan_serializer = LoanSerializer(loans, many=True)
 
    # Construct the response data
    response_data = []

    for loan in loan_serializer.data:
        monthly_installment = calculate_monthly_installment( loan['loan_amount'], loan['interest_rate'],loan['tenure'])         
        response_data.append({
            'loan_id': loan['id'],
            'loan_amount': loan['loan_amount'],
            'interest_rate': loan['interest_rate'],
            'monthly_installment': monthly_installment,  
            'repayments_left': loan['tenure'] - loan['emis_paid_on_time'],
        })

    return Response(response_data, status=status.HTTP_200_OK)