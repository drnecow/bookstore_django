# Generated by Django 4.0.4 on 2022-05-05 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentcard',
            name='expiration_date',
            field=models.CharField(max_length=10),
        ),
    ]