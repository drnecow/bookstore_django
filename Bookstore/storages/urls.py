from django.urls import path

from storages.views import AllStoragesViewSet, SpecificStorageViewSet, StorageEntryAPIView

urlpatterns = [
    path('storages/', AllStoragesViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('storages/<int:storage_id>', SpecificStorageViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('storage_entries/', StorageEntryAPIView.as_view()),
    path('storage_entries/<int:storage_entry_id>/', StorageEntryAPIView.as_view())
]