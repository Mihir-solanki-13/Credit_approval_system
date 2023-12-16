# customer/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('create-loan/', create_loan, name='create_loan'),
    path('check-eligibility/', check_eligibility, name='check_eligibility'),
    path('view-loan/<int:loan_id>/', view_loan, name='view_loan'),
    path('view-loans/<int:customer_id>/', view_loans, name='view_loans'),
]
