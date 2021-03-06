# Generated by Django 4.0.4 on 2022-05-05 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        ('storages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contract_conclusion_date', models.DateField()),
                ('contract_expiration_date', models.DateField()),
                ('available_cities', models.ManyToManyField(to='storages.city')),
            ],
            options={
                'verbose_name': 'Поставщик',
                'verbose_name_plural': 'Поставщики',
                'db_table': 'suppliers',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SupplyStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name': 'Статус поставки',
                'verbose_name_plural': 'Статусы поставки',
                'db_table': 'supply_statuses',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SupplyEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_date', models.DateField()),
                ('due_date', models.DateField()),
                ('destination_storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storages.storage')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supply.supplystatus')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supply.supplier')),
            ],
            options={
                'verbose_name': 'Запись о поставке',
                'verbose_name_plural': 'Записи о поставке',
                'db_table': 'supply_entries',
                'ordering': ['-scheduled_date'],
            },
        ),
        migrations.CreateModel(
            name='SuppliedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_books', models.PositiveIntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('related_supply_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supply.supplyentry')),
            ],
            options={
                'verbose_name': 'Поставляемая книга',
                'verbose_name_plural': 'Поставляемые книги',
                'db_table': 'supplied_books',
            },
        ),
    ]
