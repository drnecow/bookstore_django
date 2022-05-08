from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer, StringRelatedField, PrimaryKeyRelatedField

from supply.models import SupplyStatus, Supplier, SupplyEntry, SuppliedBook
from storages.models import Storage
from books.models import Book

from storages.serializers import CitySerializer, StorageSerializer
from books.serializers import ConciseBookSerializer


# Serializer for SupplyStatus model
class SupplyStatusSerializer(ModelSerializer):
    class Meta:
        model = SupplyStatus
        fields = '__all__'


# Serializer for Supplier model
class SupplierSerializer(ModelSerializer):
    available_cities = CitySerializer(many=True)

    class Meta:
        model = Supplier
        fields = '__all__'


# Serializer for SupplyEntry model, only retrieves information
class ReadOnlySupplyEntrySerializer(ModelSerializer):
    supplier = StringRelatedField(read_only=True)
    destination_storage = PrimaryKeyRelatedField(read_only=True)
    status = StringRelatedField(read_only=True)

    class Meta:
        model = SupplyEntry
        fields = '__all__'


# Serializer for SupplyEntry model, dedicated to creation requests
class CreationSupplyEntrySerializer(ModelSerializer):
    supplier = SupplierSerializer()
    destination_storage = StorageSerializer()
    status = SupplyStatusSerializer()

    class Meta:
        model = SupplyEntry
        fields = '__all__'

    def create(self, validated_data):
        supplier = get_object_or_404(Supplier, pk=validated_data.get('supplier').get('id'))
        destination_storage = get_object_or_404(Storage, pk=validated_data.get('destination_storage').get('id'))
        status = get_object_or_404(SupplyStatus, pk=validated_data.get('status').get('id'))

        new_supply_entry = SupplyEntry.objects.create(supplier=supplier, destination_storage=destination_storage,
                                                      status=status, id=validated_data.get('id'),
                                                      scheduled_date=validated_data.get('scheduled_date'),
                                                      due_date=validated_data.get('due_date'))

        return new_supply_entry

    def update(self, instance, validated_data):
        supplier_exists = validated_data.get('supplier', False)
        if supplier_exists:
            supplier = get_object_or_404(Supplier, pk=validated_data.get('supplier').get('id', 0))
            instance.supplier = supplier

        destination_storage_exists = validated_data.get('destination_storage', False)
        if destination_storage_exists:
            destination_storage = get_object_or_404(Storage, pk=validated_data.get('destination_storage').get('id', 0))
            instance.destination_storage = destination_storage

        status_exists = validated_data.get('status', False)
        if status_exists:
            status = get_object_or_404(SupplyStatus, pk=validated_data.get('status').get('id', 0))
            instance.status = status

        instance.scheduled_date = validated_data.get('scheduled_date', instance.scheduled_date)
        instance.due_date = validated_data.get('due_date', instance.due_date)

        instance.save()

        return instance


# Serializer for SuppliedBook model
class SuppliedBookSerializer(ModelSerializer):
    related_supply_entry = ReadOnlySupplyEntrySerializer()
    book = ConciseBookSerializer()

    class Meta:
        model = SuppliedBook
        fields = '__all__'

    def create(self, validated_data):
        related_supply_entry = get_object_or_404(SupplyEntry, pk=validated_data.get('related_supply_entry').get('id'))
        book = get_object_or_404(Book, pk=validated_data.get('book').get('id'))

        new_supplied_book_entry = SuppliedBook.objects.create(related_supply_entry=related_supply_entry, book=book,
                                                              id=validated_data.get('id'),
                                                              number_of_books=validated_data.get('number_of_books'))

        return new_supplied_book_entry

    def update(self, instance, validated_data):

        instance.number_of_books = validated_data.get('number_of_books', instance.number_of_books)

        instance.save()

        return instance
