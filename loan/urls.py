# customer/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('create_loan/', create_loan, name='create_loan'),
]
