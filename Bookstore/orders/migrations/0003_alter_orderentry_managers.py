# Generated by Django 4.0.4 on 2022-05-05 16:40

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='orderentry',
            managers=[
                ('entries', django.db.models.manager.Manager()),
            ],
        ),
    ]
