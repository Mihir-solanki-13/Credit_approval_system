# credit_app/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Customer
from .serializers import *
from django.utils import timezone


@api_view(['POST'])
def register_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        monthly_income = data['monthly_income']

        # Calculate approved limit based on the given formula
        approved_limit = round(36 * monthly_income / 100000) * 100000

        # Create a new customer
        customer = Customer.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data['age'],
            monthly_income=monthly_income,
            approved_limit=approved_limit,
            phone_number=data['phone_number'],
        )

        response_data = {
            'customer_id': customer.id,
            'name': f"{customer.first_name} {customer.last_name}",
            'age': customer.age,
            'monthly_income': customer.monthly_income,
            'approved_limit': customer.approved_limit,
            'phone_number': customer.phone_number
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


