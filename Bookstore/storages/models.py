from django.db import models

from books.admin import Book
from storages.managers import StorageQuerySet


# One of Kazakhstan's cities
class City(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        db_table = 'cities'
        ordering = ['name']

    def __str__(self):
        return self.name


# Store's storages located in different cities of Kazakhstan
class Storage(models.Model):
    location_city = models.ForeignKey(to=City, on_delete=models.CASCADE, related_name='location_cities')
    address = models.CharField(max_length=200)
    is_functional = models.BooleanField(default=True)
    delivery_available_cities = models.ManyToManyField(to=City, related_name='delivery_available_cities')

    objects = models.Manager()
    storages = StorageQuerySet.as_manager()

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'
        db_table = 'storages'
        ordering = ['id']

    def __str__(self):
        return f'Storage {self.pk}'


# Entry about a number of instances of each book stored at a specific storage
class StorageEntry(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    storage = models.ForeignKey(to=Storage, on_delete=models.CASCADE)
    number_of_books = models.PositiveIntegerField()
    last_updated = models.DateField()

    class Meta:
        verbose_name = 'Запись о хранении'
        verbose_name_plural = 'Записи о хранении'
        db_table = 'storage_entries'
        ordering = ['-last_updated']

    def __str__(self):
        return f'Storage entry {self.pk}'
