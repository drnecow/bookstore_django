from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer, StringRelatedField

from storages.models import City, Storage, StorageEntry
from books.models import Book
from books.serializers import ConciseBookSerializer

import datetime

# Serializer for City model
class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


# Serializer for Storage model
class StorageSerializer(ModelSerializer):
    location_city = CitySerializer()
    delivery_available_cities = CitySerializer(many=True)

    class Meta:
        model = Storage
        fields = '__all__'

    def create(self, validated_data):
        location_city = validated_data.get('location_city')
        delivery_available_cities = validated_data.get('delivery_available_cities')

        location_city, created = City.objects.get_or_create(**location_city)

        storage = Storage.objects.create(location_city=location_city, id=validated_data.get('id'),
                                         address=validated_data.get('address'),
                                         is_functional=validated_data.get('is_functional'))

        for city in delivery_available_cities:
            city, created = City.objects.get_or_create(**city)
            storage.delivery_available_cities.add(city)

        return storage

    def update(self, instance, validated_data):
        if validated_data.get('delivery_available_cities', False):
            delivery_available_cities = validated_data.pop('delivery_available_cities')
            instance.delivery_available_cities.set([])
            for city in delivery_available_cities:
                city, created = City.objects.get_or_create(**city)
                instance.delivery_available_cities.add(city)

        instance.address = validated_data.get('address', instance.address)
        instance.is_functional = validated_data.get('is_functional', instance.is_functional)

        instance.save()

        return instance


# More concise information about Storage
class ConciseStorageSerializer(ModelSerializer):
    location_city = CitySerializer()

    class Meta:
        model = Storage
        fields = ['id', 'location_city', 'is_functional']


# Serializer for StorageEntry model
class StorageEntrySerializer(ModelSerializer):
    book = ConciseBookSerializer()
    storage = ConciseStorageSerializer()

    class Meta:
        model = StorageEntry
        fields = '__all__'

    def create(self, validated_data):
        book = get_object_or_404(Book, pk=validated_data.get('book').get('id'))
        storage = get_object_or_404(Storage, pk=validated_data.get('storage').get('id'))

        new_storage_entry = StorageEntry.objects.create(id=validated_data.get('id'), book=book, storage=storage,
                                                        number_of_books=validated_data.get('number_of_books'),
                                                        last_updated=datetime.date.today())

        return new_storage_entry

    def update(self, instance, validated_data):
        instance.number_of_books = validated_data.get('number_of_books', instance.number_of_books)
        instance.last_updated = datetime.date.today()

        instance.save()

        return instance
