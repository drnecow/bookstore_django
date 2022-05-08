from django.db import models

from user.models import UserOrderAddress, BookstoreUser
from books.models import Book
from orders.validators import validate_reception_type
from orders.managers import OrderEntryQuerySet


# One of fixed order statuses: 1 — in assembly, 2 — waiting for payment, 3 — waiting for delivery, ...
# ...4 — late, 5 — delivered, 6 — cancelled
class OrderStatus(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'
        db_table = 'order_statuses'
        ordering = ['id']

    def __str__(self):
        return f'{self.pk} — {self.name}'


# Entry of an order made by a user.
class OrderEntry(models.Model):
    customer = models.ForeignKey(to=BookstoreUser, on_delete=models.CASCADE)
    address = models.ForeignKey(to=UserOrderAddress, on_delete=models.CASCADE)
    order_date = models.DateField()
    maximum_delivery_date = models.DateField(null=True)
    reception_type = models.CharField(max_length=10, validators=[validate_reception_type])
    status = models.ForeignKey(to=OrderStatus, on_delete=models.CASCADE)

    objects = models.Manager()
    entries = OrderEntryQuerySet.as_manager()

    class Meta:
        verbose_name = 'Запись о заказе'
        verbose_name_plural = 'Записи о заказе'
        db_table = 'order_entries'
        ordering = ['-order_date']

    def __str__(self):
        return f'Order entry {self.pk}'


# What books exactly are being supplied in a particular entry.
class OrderedBook(models.Model):
    related_order_entry = models.ForeignKey(to=OrderEntry, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    number_of_books = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Заказанная книга'
        verbose_name_plural = 'Заказанные книги'
        db_table = 'ordered_books'

    def __str__(self):
        return f'Ordered book "{self.book.name}" in order {self.related_order_entry.id}, id: {self.pk}'
