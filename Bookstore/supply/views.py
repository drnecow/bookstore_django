from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from supply.models import SupplyStatus, Supplier, SupplyEntry, SuppliedBook
from supply.serializers import (SupplyStatusSerializer, ReadOnlySupplyEntrySerializer, SupplierSerializer,
                                CreationSupplyEntrySerializer, SuppliedBookSerializer)

import logging

logger = logging.getLogger(__name__)


# Returns all existing supply statuses and allows superusers to create new ones
class SupplyStatusesAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        supply_statuses = SupplyStatus.objects.all()
        serializer = SupplyStatusSerializer(supply_statuses, many=True)

        logger.debug(f"All supply statuses viewed by {request.user.username} user: SupplyStatusesAPIView API")
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_superuser:
            return Response({"message": "Access denied."})

        serializer = SupplyStatusSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            logger.debug(f"New supply status '{serializer.data.get('name')}' created by {request.user.username} user: SupplyStatusesAPIView API")
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, status_id):
        if not request.user.is_superuser:
            return Response({"message": "Access denied."})

        status = SupplyStatus.objects.filter(id=status_id).first()
        if status:
            status.delete()
            logger.debug(f"Supply status with id {status_id} successfully deleted by {request.user.username} user: SupplyStatusesAPIView API")
            return Response({"message": "Supply status successfully deleted."}, status=204)
        else:
            return Response({"message": "Supply status to delete not found."}, status=404)


# View all supply entries and create new one
class AllSupplyEntriesViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return SupplyEntry.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ReadOnlySupplyEntrySerializer(queryset, many=True)

        logger.debug(f"All supply entries viewed by {request.user.username}: AllSupplyEntriesViewSet API")
        return Response(serializer.data)

    def create(self, request):
        created_supply_entry = CreationSupplyEntrySerializer.create(self=CreationSupplyEntrySerializer(), validated_data=request.data)
        created_supply_entry.save()

        logger.debug(f"New supply entry with id '{created_supply_entry.id}' created by {request.user.username} "
                             f"user: AllSupplyEntriesViewSet API")
        return Response(request.data)


# Retrieve or update specific order entry
class SpecificSupplyEntryViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    def get_supply_entry(self, supply_entry_id):
        return SupplyEntry.objects.filter(id=supply_entry_id).first()

    def retrieve(self, request, supply_entry_id):
        supply_entry = self.get_supply_entry(supply_entry_id=supply_entry_id)
        if supply_entry:
            serializer = ReadOnlySupplyEntrySerializer(supply_entry)

            logger.debug(f"Supply entry with id {supply_entry_id} viewed: SpecificSupplyEntryViewSet API")
            return Response(serializer.data)
        else:
            return Response({"message": "Supply entry not found."}, status=404)

    def update(self, request, supply_entry_id):
        if not request.user.is_staff:
            return Response({"message": "Access denied."})

        supply_entry = self.get_supply_entry(supply_entry_id=supply_entry_id)
        if supply_entry:
            serializer = CreationSupplyEntrySerializer(CreationSupplyEntrySerializer.update(self=CreationSupplyEntrySerializer(),
                                                                              instance=supply_entry, validated_data=request.data))
            logger.debug(f"Supply entry with id {supply_entry_id} updated by {request.user.username} user: SpecificSupplyEntryViewSet API")
            return Response(serializer.data)

        else:
            return Response({"message": "Supply entry to update not found."}, status=404)


# Create, retrieve and update SuppliedBook entry
class SuppliedBookAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, supplied_book_id):
        supplied_book = SuppliedBook.objects.filter(id=supplied_book_id).first()
        if supplied_book:
            serializer = SuppliedBookSerializer(supplied_book)
            logger.debug(f"Supplied book entry viewed by {request.user.username} user: SuppliedBookAPIView API")
            return Response(serializer.data)
        else:
            return Response({"message": "Supplied book entry not found."}, status=404)

    def post(self, request):
        created_supplied_book = SuppliedBookSerializer.create(self=SuppliedBookSerializer(), validated_data=request.data)
        created_supplied_book.save()

        logger.debug(f"New supplied book entry with id '{created_supplied_book.id}' created by {request.user.username} "
                     f"user: SuppliedBookAPIView API")
        return Response(request.data)

    def put(self, request, supplied_book_id):
        supplied_book = SuppliedBook.objects.filter(id=supplied_book_id).first()
        if supplied_book:
            serializer = SuppliedBookSerializer(SuppliedBookSerializer.update(self=SuppliedBookSerializer(),
                                                    instance=supplied_book, validated_data=request.data))
            logger.debug(
                f"Ordered book entry with id {supplied_book_id} updated by {request.user.username} user: SuppliedBookAPIView API")
            return Response(serializer.data)

    def delete(self, request, supplied_book_id):
        supplied_book = SuppliedBook.objects.filter(id=supplied_book_id).first()
        if supplied_book:
            supplied_book.delete()
            logger.debug(f"Supplied book entry with id {supplied_book_id} successfully deleted by {request.user.username} "
                         f"user: SuppliedBookAPIView API")
            return Response({"message": "Supplied book entry successfully deleted."}, status=204)
        else:
            return Response({"message": "Supplied book entry to delete not found."}, status=404)
