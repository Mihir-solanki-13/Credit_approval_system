# Generated by Django 4.0 on 2023-12-16 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_remove_customer_credit_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='current_debt',
        ),
        migrations.AlterField(
            model_name='customer',
            name='age',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='customer',
            name='approved_limit',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='customer',
            name='monthly_income',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.BigIntegerField(),
        ),
    ]
