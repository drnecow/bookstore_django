from django.urls import path

from books.views import AllBooksViewSet, SpecificBookViewSet

urlpatterns = [
    path('books/', AllBooksViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('books/<int:book_id>/', SpecificBookViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))
]