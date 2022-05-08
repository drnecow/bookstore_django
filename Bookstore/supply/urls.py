from django.urls import path

from supply.views import SupplyStatusesAPIView, AllSupplyEntriesViewSet, SpecificSupplyEntryViewSet, SuppliedBookAPIView

urlpatterns = [
    path('supply_statuses/', SupplyStatusesAPIView.as_view()),
    path('supply_statuses/<int:status_id>/', SupplyStatusesAPIView.as_view()),
    path('supply_entries/', AllSupplyEntriesViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('supply_entries/<int:supply_entry_id>/', SpecificSupplyEntryViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('supplied_books/', SuppliedBookAPIView.as_view()),
    path('supplied_books/<int:supplied_book_id>/', SuppliedBookAPIView.as_view())
]
