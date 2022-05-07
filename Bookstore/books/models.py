from django.db import models

from books.validators import validate_cover_image, validate_isbn


# Book's publisher
class Publisher(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'
        db_table = 'publishers'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, id: {self.id}'


# Book's author or authors
class Author(models.Model):
    first_name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        db_table = 'authors'
        ordering = ['surname']

    def __str__(self):
        return f'{self.surname} {self.first_name}, id: {self.id}'


# Book's genres
class Genre(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        db_table = 'genres'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, id: {self.id}'


# Book, the store's ultimate commodity
class Book(models.Model):
    name = models.CharField(max_length=300)
    isbn = models.CharField(max_length=13, validators=[validate_isbn])
    publisher = models.ForeignKey(to=Publisher, on_delete=models.CASCADE)
    authors = models.ManyToManyField(to=Author)
    genres = models.ManyToManyField(to=Genre)
    date_published = models.DateField()
    price = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='book_cover_images/', null=True, validators=[validate_cover_image])

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        db_table = 'books'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, id: {self.id}'
