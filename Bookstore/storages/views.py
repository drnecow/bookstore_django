from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from storages.models import Storage, StorageEntry
from storages.serializers import StorageSerializer, StorageEntrySerializer

import logging

logger = logging.getLogger(__name__)


# View all storages and create new ones
class AllStoragesViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return Storage.objects.all()

    def get_storage(self, storage_id):
        return Storage.objects.filter(id=storage_id).first()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = StorageSerializer(queryset, many=True)

        logger.debug(f"All storages viewed by {request.user.username}: AllStoragesViewSet API")
        return Response(serializer.data)

    def create(self, request):
        if not request.user.is_superuser:
            return Response({"message": "Access denied: not superuser."})

        created_storage = StorageSerializer.create(self=StorageSerializer(), validated_data=request.data)
        created_storage.save()

        logger.debug(f"New storage with id '{created_storage.id}' created by {request.user.username} "
                     f"user: AllStoragesViewSet API")
        return Response(request.data)


# View and update specific storages
class SpecificStorageViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    def get_storage(self, storage_id):
        return Storage.objects.filter(id=storage_id).first()

    def retrieve(self, request, storage_id):
        storage = self.get_storage(storage_id=storage_id)
        if storage:
            serializer = StorageSerializer(storage)

            logger.debug(f"Storage with id {storage_id} viewed: SpecificStorageViewSet API")
            return Response(serializer.data)
        else:
            return Response({"message": "Storage not found."}, status=404)

    def update(self, request, storage_id):
        if not request.user.is_superuser:
            return Response({"message": "Access denied: not superuser."})

        storage = self.get_storage(storage_id=storage_id)
        if storage:
            serializer = StorageSerializer(StorageSerializer.update(self=StorageSerializer(), instance=storage,
                                                                    validated_data=request.data))
            logger.debug(
                f"Storage with id {storage_id} updated by {request.user.username} user: SpecificStorageViewSet API")
            return Response(serializer.data)

        else:
            return Response({"message": "Storage to update not found."}, status=404)


# Create, retrieve and update StorageEntry
class StorageEntryAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, storage_entry_id):
        storage_entry = StorageEntry.objects.filter(id=storage_entry_id).first()
        if storage_entry:
            serializer = StorageEntrySerializer(storage_entry)
            logger.debug(f"Storage entry viewed by {request.user.username} user: StorageEntryAPIView API")
            return Response(serializer.data)
        else:
            return Response({"message": "Storage entry not found."}, status=404)

    def post(self, request):
        created_storage_entry = StorageEntrySerializer.create(self=StorageEntrySerializer(), validated_data=request.data)
        created_storage_entry.save()

        logger.debug(f"New storage entry with id '{created_storage_entry.id}' created by {request.user.username} "
                     f"user: StorageEntryAPIView API")
        return Response(request.data)

    def put(self, request, storage_entry_id):
        storage_entry = StorageEntry.objects.filter(id=storage_entry_id).first()
        if storage_entry:
            serializer = StorageEntrySerializer(
                StorageEntrySerializer.update(self=StorageEntrySerializer(), instance=storage_entry,
                                              validated_data=request.data))
            logger.debug(
                f"Storage entry with id {storage_entry_id} updated by {request.user.username} user: StorageEntryAPIView API")
            return Response(serializer.data)

    def delete(self, request, storage_entry_id):
        storage_entry = StorageEntry.objects.filter(id=storage_entry_id).first()
        if storage_entry:
            storage_entry.delete()
            logger.debug(f"Ordered book entry with id {storage_entry_id} successfully deleted by {request.user.username} "
                         f"user: StorageEntryAPIView API")
            return Response({"message": "Storage entry successfully deleted."}, status=204)
        else:
            return Response({"message": "Storage entry to delete not found."}, status=404)
