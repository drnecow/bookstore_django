from django.db import models

from storages.models import City, Storage
from books.models import Book
from supply.managers import SupplyEntryQuerySet


# One of fixed supply statuses: 1 — waiting for delivery, 2 — late, 3 — delivered, 4 — cancelled
class SupplyStatus(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        verbose_name = 'Статус поставки'
        verbose_name_plural = 'Статусы поставки'
        db_table = 'supply_statuses'
        ordering = ['id']

    def __str__(self):
        return f'{self.pk} — {self.name}'


# Organization the store buys books from
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contract_conclusion_date = models.DateField()
    contract_expiration_date = models.DateField()
    available_cities = models.ManyToManyField(to=City)

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        db_table = 'suppliers'
        ordering = ['name']

    def __str__(self):
        return self.name


# Entry of a supply ordered by a store from a specific supplier.
class SupplyEntry(models.Model):
    supplier = models.ForeignKey(to=Supplier, on_delete=models.CASCADE)
    destination_storage = models.ForeignKey(to=Storage, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    due_date = models.DateField()
    status = models.ForeignKey(to=SupplyStatus, on_delete=models.CASCADE)

    entries = SupplyEntryQuerySet.as_manager()

    class Meta:
        verbose_name = 'Запись о поставке'
        verbose_name_plural = 'Записи о поставке'
        db_table = 'supply_entries'
        ordering = ['-scheduled_date']

    def __str__(self):
        return f'Supply entry {self.pk}'


# What books exactly are being supplied in a particular entry.
class SuppliedBook(models.Model):
    related_supply_entry = models.ForeignKey(to=SupplyEntry, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    number_of_books = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Поставляемая книга'
        verbose_name_plural = 'Поставляемые книги'
        db_table = 'supplied_books'

    def __str__(self):
        return f'Supplied book "{self.book.name}" in entry {self.related_supply_entry.primary_key}'
