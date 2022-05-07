from rest_framework.serializers import ModelSerializer, StringRelatedField
from user.models import BookstoreUser, UserOrderAddress


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
