# Generated by Django 4.0.4 on 2022-05-05 15:20

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('storages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookstoreUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'db_table': 'bookstore_users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brief_name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('creation_date', models.DateField()),
                ('expiration_date', models.DateField(null=True)),
            ],
            options={
                'verbose_name': 'Купон',
                'verbose_name_plural': 'Купоны',
                'db_table': 'coupons',
                'ordering': ['creation_date'],
            },
        ),
        migrations.CreateModel(
            name='UserOrderAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('city', models.ManyToManyField(to='storages.city')),
            ],
            options={
                'verbose_name': 'Адрес заказа',
                'verbose_name_plural': 'Адреса заказа',
                'db_table': 'order_addresses',
            },
        ),
        migrations.CreateModel(
            name='PaymentCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_account_number', models.CharField(max_length=16)),
                ('cardholder_name', models.CharField(max_length=100)),
                ('expiration_date', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Платёжная карта',
                'verbose_name_plural': 'Платёжные карты',
                'db_table': 'payment_cards',
            },
        ),
        migrations.AddField(
            model_name='bookstoreuser',
            name='user_addresses',
            field=models.ManyToManyField(related_name='user_addresses', to='user.userorderaddress'),
        ),
        migrations.AddField(
            model_name='bookstoreuser',
            name='user_coupons',
            field=models.ManyToManyField(related_name='user_coupons', to='user.coupon'),
        ),
        migrations.AddField(
            model_name='bookstoreuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='bookstoreuser',
            name='user_wishlist',
            field=models.ManyToManyField(related_name='user_wishlist', to='books.book'),
        ),
    ]
