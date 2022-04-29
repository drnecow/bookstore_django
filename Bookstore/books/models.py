from django.db import models


# Book's publisher
class Publisher(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'
        db_table = 'publishers'
        ordering = ['name']

    def __str__(self):
        return self.name


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
        return f'{self.surname} + {self.first_name}'


# Book's genres
class Genre(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        db_table = 'genres'
        ordering = ['name']

    def __str__(self):
        return self.name


# Book, the store's ultimate commodity
class Book(models.Model):
    name = models.CharField(max_length=300)
    isbn = models.CharField(max_length=13)
    publisher = models.ForeignKey(to=Publisher, on_delete=models.CASCADE)
    authors = models.ManyToManyField(to=Author)
    genres = models.ManyToManyField(to=Genre)
    date_published = models.DateField()
    price = models.PositiveIntegerField()
    # cover_image = models.ImageField()

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        db_table = 'books'
        ordering = ['name']

    def __str__(self):
        return self.name
