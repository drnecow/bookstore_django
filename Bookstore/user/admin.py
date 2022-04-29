from django.contrib import admin
from user.models import UserOrderAddress, BookstoreUser, Coupon, PaymentCard

# Register your models here.
admin.site.register(UserOrderAddress)
admin.site.register(BookstoreUser)
admin.site.register(Coupon)
admin.site.register(PaymentCard)
