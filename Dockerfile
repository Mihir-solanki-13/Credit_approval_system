FROM python:3.11.4-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY . /app/
COPY customer_data.xlsx /app/customer_data.xlsx
COPY loan_data.xlsx /app/loan_data.xlsx
COPY import_loan_data.py /app/import_loan_data.py

RUN apt-get update

COPY ./requirements.txt .
RUN pip install -r requirements.txt
