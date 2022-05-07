from django.urls import path

from orders.views import OrderStatusesAPIView, AllOrderEntriesViewSet, SpecificOrderEntryViewSet, OrderedBookAPIView

urlpatterns = [
    path('order_statuses/', OrderStatusesAPIView.as_view()),
    path('order_statuses/<int:status_id>/', OrderStatusesAPIView.as_view()),
    path('order_entries/', AllOrderEntriesViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('order_entries/<int:order_entry_id>/', SpecificOrderEntryViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('ordered_books/', OrderedBookAPIView.as_view()),
    path('ordered_books/<int:ordered_book_id>/', OrderedBookAPIView.as_view())
]
