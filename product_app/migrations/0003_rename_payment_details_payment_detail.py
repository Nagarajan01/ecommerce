# Generated by Django 4.1 on 2022-11-09 05:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product_app', '0002_payment_details'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Payment_Details',
            new_name='Payment_Detail',
        ),
    ]