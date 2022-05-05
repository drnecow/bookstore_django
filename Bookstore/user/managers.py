from django.db import models
from datetime import date


# Manager for BookstoreUser model
class BookstoreUserQuerySet(models.QuerySet):
    def all(self):
        return self

    def regular_users(self):
        return self.filter(is_staff=False)

    def staff(self):
        return self.filter(is_staff=True)

    def superusers(self):
        return self.filter(is_superuser=True)

    def active(self):
        return self.filter(is_staff=False, is_active=True)


# Manager for Coupon model
class CouponQuerySet(models.QuerySet):
    def all(self):
        return self

    def active(self):
        return self.filter(expiration_date__gt=date.today())

    def expired(self):
        return self.filter(expiration_date__lte=date.today())
