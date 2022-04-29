from django.contrib import admin
from books.models import Publisher, Author, Genre, Book

# Register your models here.
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
