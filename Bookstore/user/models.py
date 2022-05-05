from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

from storages.models import City
from books.models import Book
from user.managers import BookstoreUserQuerySet, CouponQuerySet


# User's address to which order should be delivered.
class UserOrderAddress(models.Model):
    description = models.CharField(max_length=200)
    city = models.ManyToManyField(to=City)

    class Meta:
        verbose_name = 'Адрес заказа'
        verbose_name_plural = 'Адреса заказа'
        db_table = 'order_addresses'

    def __str__(self):
        return self.description


# Coupons owned by user
class Coupon(models.Model):
    brief_name = models.CharField(max_length=150)
    description = models.TextField()
    creation_date = models.DateField()
    expiration_date = models.DateField(null=True)

    coupons = CouponQuerySet.as_manager()

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'
        db_table = 'coupons'
        ordering = ['creation_date']

    def __str__(self):
        return self.brief_name


# Project's user model
class BookstoreUser(AbstractUser):
    user_wishlist = models.ManyToManyField(to=Book, related_name='user_wishlist')
    user_addresses = models.ManyToManyField(to=UserOrderAddress, related_name='user_addresses')
    user_coupons = models.ManyToManyField(to=Coupon, related_name='user_coupons')

    users = BookstoreUserQuerySet.as_manager()

    # This field requires implementing hashing first.
    # user_payment_cards = models.ManyToManyField(to=PaymentCard, related_name='user_payment_cards')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'bookstore_users'


# User's payment card, in case they wish to save any.
# Only information stored is PAN, cardholder name and expiration date.
# In production, it must be stored in encrypted format, as dictated by PCI DSS.
class PaymentCard(models.Model):
    primary_account_number = models.CharField(max_length=128)
    cardholder_name = models.CharField(max_length=128)
    expiration_date = models.CharField(max_length=128)
    owner = models.ForeignKey(to=BookstoreUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Платёжная карта'
        verbose_name_plural = 'Платёжные карты'
        db_table = 'payment_cards'

    def __str__(self):
        return f'Card {self.pk} owned by {self.owner.username}'

    def save(self, **kwargs):
        salt = 'IJFife0-2UJF__feo03rfjeiaKlds'
        self.primary_account_number = make_password(self.primary_account_number, salt=salt)
        self.cardholder_name = make_password(self.cardholder_name, salt=salt)
        self.expiration_date = make_password(self.expiration_date, salt=salt)
        super().save(**kwargs)
