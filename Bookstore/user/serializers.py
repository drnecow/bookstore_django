from rest_framework.serializers import ModelSerializer, StringRelatedField

from user.models import BookstoreUser, UserOrderAddress, Coupon
from books.serializers import ConciseBookSerializer


# Serializer for viewing users in other models
class ConciseUserSerializer(ModelSerializer):
    class Meta:
        model = BookstoreUser
        fields = ['id', 'username', 'email']


# Serializer for UserOrderAddress model
class UserOrderAddressSerializer(ModelSerializer):
    city = StringRelatedField()

    class Meta:
        model = UserOrderAddress
        fields = '__all__'


# Serializer for Coupon model
class CouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


# Serializer for viewing BookstoreUser entry itself
class DetailedUserSerializer(ModelSerializer):
    user_wishlist = ConciseBookSerializer(read_only=True)
    user_addresses = UserOrderAddressSerializer(read_only=True)
    user_coupons = CouponSerializer(read_only=True)

    class Meta:
        model = BookstoreUser
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser', 'user_addresses',
                  'user_coupons', 'date_joined', 'last_login']
