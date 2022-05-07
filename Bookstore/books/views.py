from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from books.models import Book
from books.serializers import ConciseBookSerializer, DetailedBookSerializer

import logging

logger = logging.getLogger(__name__)


# Returns all books in the database to view and allows to create new books
class AllBooksViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Book.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ConciseBookSerializer(queryset, many=True)

        logger.debug("All books viewed: AllBooksViewSet API")
        return Response(serializer.data)

    def create(self, request):
        if not request.user.is_staff:
            return Response({"message": "Access denied."})

        serializer = DetailedBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            logger.debug(f"New book '{serializer.data.get('name')}' created by {request.user.username} user: AllBooksViewSet API")
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


# Returns a specific book from a database to view and allows to update it as well
class SpecificBookViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def get_book(self, book_id):
        return Book.objects.filter(id=book_id).first()

    def retrieve(self, request, book_id):
        book = self.get_book(book_id=book_id)
        if book:
            serializer = DetailedBookSerializer(book)

            logger.debug(f"Book with id {book_id} viewed: SpecificBookViewSet API")
            return Response(serializer.data)
        else:
            return Response({"message": "Book not found."}, status=404)

    def update(self, request, book_id):
        if not request.user.is_staff:
            return Response({"message": "Access denied."})

        book = self.get_book(book_id=book_id)
        if book:
            serializer = DetailedBookSerializer(DetailedBookSerializer.update(self=DetailedBookSerializer(),
                                                                              instance=book, validated_data=request.data))
            logger.debug(f"Book with id {book_id} updated by {request.user.username} user: SpecificBookViewSet API")
            return Response(serializer.data)

        else:
            return Response({"message": "Book to update not found."}, status=404)

    def destroy(self, request, book_id):
        if not request.user.is_superuser:
            return Response({"message": "Access denied."})

        book = self.get_book(book_id=book_id)
        if book:
            book.delete()

            logger.debug(f"Book with id {book_id} successfully deleted by {request.user.username}: SpecificBookViewSet API")
            return Response({"message": "Book successfully deleted."}, status=204)
        else:
            return Response({"message": "Book to delete not found."}, status=404)
