# Generated by Django 4.0.4 on 2022-05-05 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_paymentcard_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentcard',
            name='cardholder_name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='paymentcard',
            name='expiration_date',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='paymentcard',
            name='primary_account_number',
            field=models.CharField(max_length=128),
        ),
    ]
