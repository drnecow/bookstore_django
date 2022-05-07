from rest_framework.serializers import ModelSerializer, StringRelatedField
from books.models import Author, Publisher, Genre, Book


# Serializer for Author model
class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


# Serializer for Publisher model
class PublisherSerializer(ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


# Serializer for Genre model
class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


# Serializer for retrieving all objects of Book model. More concise information
class ConciseBookSerializer(ModelSerializer):
    authors = StringRelatedField(many=True, read_only=True)
    publisher = StringRelatedField(read_only=True)
    genres = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'authors', 'publisher', 'genres']


# Serializer for retrieving, updating or creating a specific object of Book model. More detailed information
class DetailedBookSerializer(ModelSerializer):
    authors = AuthorSerializer(many=True)
    publisher = PublisherSerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        authors = validated_data.pop('authors')
        genres = validated_data.pop('genres')
        publisher = validated_data.pop('publisher')

        publisher, created = Publisher.objects.get_or_create(**publisher)

        book = Book.objects.create(publisher=publisher, **validated_data)

        for author in authors:
            author, created = Author.objects.get_or_create(**author)
            book.authors.add(author)

        for genre in genres:
            genre, created = Genre.objects.get_or_create(**genre)
            book.genres.add(genre)

        return book

    def update(self, instance, validated_data):
        if validated_data.get('authors', False):
            authors = validated_data.pop('authors')
            instance.authors.set([])
            for author in authors:
                author, created = Author.objects.get_or_create(**author)
                instance.authors.add(author)

        if validated_data.get('genres', False):
            genres = validated_data.pop('genres')
            instance.genres.set([])
            for genre in genres:
                genre, created = Genre.objects.get_or_create(**genre)
                instance.genres.add(genre)

        if validated_data.get('publisher', False):
            publisher = validated_data.pop('publisher')
            publisher, created = Publisher.objects.get_or_create(**publisher)
            instance.publisher = publisher

        instance.name = validated_data.get('name', instance.name)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.date_published = validated_data.get('date_published', instance.date_published)
        instance.price = validated_data.get('price', instance.price)

        instance.save()

        return instance
