# Generated by Django 4.0 on 2023-12-16 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='credit_score',
        ),
    ]
