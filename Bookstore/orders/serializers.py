from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer, StringRelatedField, PrimaryKeyRelatedField

from orders.models import OrderStatus, OrderEntry, OrderedBook
from user.models import BookstoreUser, UserOrderAddress
from books.models import Book

from user.serializers import ConciseUserSerializer, UserOrderAddressSerializer
from books.serializers import ConciseBookSerializer


# Serializer for OrderStatus model
class OrderStatusSerializer(ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'


# Serializer for OrderEntry model, only retrieves information
class ReadOnlyOrderEntrySerializer(ModelSerializer):
    customer = ConciseUserSerializer(read_only=True)
    address = UserOrderAddressSerializer(read_only=True)
    status = StringRelatedField(read_only=True)

    class Meta:
        model = OrderEntry
        fields = '__all__'


# Serializer for OrderEntry model, dedicated to creation requests
class CreationOrderEntrySerializer(ModelSerializer):
    customer = ConciseUserSerializer()
    address = UserOrderAddressSerializer()
    status = StringRelatedField()

    class Meta:
        model = OrderEntry
        fields = '__all__'

    def create(self, validated_data):
        customer = get_object_or_404(BookstoreUser, pk=validated_data.get('customer').get('id'))
        address = get_object_or_404(UserOrderAddress, pk=validated_data.get('address').get('id'))
        status = get_object_or_404(OrderStatus, pk=validated_data.get('status').get('id'))

        new_order_entry = OrderEntry.objects.create(customer=customer, address=address, status=status, id=validated_data.get('id'),
                                                    order_date=validated_data.get('order_date'),
                                                    maximum_delivery_date=validated_data.get('maximum_delivery_date'),
                                                    reception_type=validated_data.get('reception_type'))

        return new_order_entry

    def update(self, instance, validated_data):
        customer_exists = validated_data.get('customer', False)
        if customer_exists:
            customer = get_object_or_404(BookstoreUser, pk=validated_data.get('customer').get('id', 0))
            instance.customer = customer

        address_exists = validated_data.get('address', False)
        if address_exists:
            address = get_object_or_404(UserOrderAddress, pk=validated_data.get('address').get('id', 0))
            instance.address = address

        status_exists = validated_data.get('status', False)
        if status_exists:
            status = get_object_or_404(OrderStatus, pk=validated_data.get('status').get('id', 0))
            instance.status = status

        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.maximum_delivery_date = validated_data.get('maximum_delivery_date',
                                                            instance.maximum_delivery_date)
        instance.reception_type = validated_data.get('reception_type', instance.reception_type)

        instance.save()

        return instance


# Serializer for OrderedBook model
class OrderedBookSerializer(ModelSerializer):
    related_order_entry = ReadOnlyOrderEntrySerializer()
    book = ConciseBookSerializer()

    class Meta:
        model = OrderedBook
        fields = '__all__'

    def create(self, validated_data):
        related_order_entry = get_object_or_404(OrderEntry, pk=validated_data.get('related_order_entry').get('id'))
        book = get_object_or_404(Book, pk=validated_data.get('book').get('id'))

        new_ordered_book_entry = OrderedBook.objects.create(related_order_entry=related_order_entry, book=book,
                                                            id=validated_data.get('id'),
                                                            number_of_books=validated_data.get('number_of_books'))

        return new_ordered_book_entry

    def update(self, instance, validated_data):

        instance.number_of_books = validated_data.get('number_of_books', instance.number_of_books)

        instance.save()

        return instance

