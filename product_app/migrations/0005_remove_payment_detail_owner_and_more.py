# Generated by Django 4.1 on 2022-11-09 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0004_payment_detail_payment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment_detail',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='payment_detail',
            name='purchaser',
        ),
    ]