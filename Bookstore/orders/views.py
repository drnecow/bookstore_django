from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from orders.models import OrderStatus, OrderEntry, OrderedBook
from orders.serializers import OrderStatusSerializer, ReadOnlyOrderEntrySerializer, CreationOrderEntrySerializer, OrderedBookSerializer

import logging

logger = logging.getLogger(__name__)


# Returns all existing user statuses and allows superusers to create new ones
class OrderStatusesAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        order_statuses = OrderStatus.objects.all()
        serializer = OrderStatusSerializer(order_statuses, many=True)

        logger.debug(f"All order statuses viewed by {request.user.username} user: OrderStatusesAPIView API")
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_superuser:
            return Response({"message": "Access denied."})

        serializer = OrderStatusSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            logger.debug(f"New order status {serializer.data.get('name')} created by {request.user.username} user: OrderStatusesAPIView API")
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, status_id):
        if not request.user.is_superuser:
            return Response({"message": "Access denied."})

        status = OrderStatus.objects.filter(id=status_id).first()
        if status:
            status.delete()
            logger.debug(f"Order status with id {status_id} successfully deleted by {request.user.username} user: OrderStatusesAPIView API")
            return Response({"message": "Order status successfully deleted."}, status=204)
        else:
            return Response({"message": "Order status to delete not found."}, status=404)


# View all order entries and create new one
class AllOrderEntriesViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return OrderEntry.objects.all()

    def list(self, request):
        if not request.user.is_staff:
            return Response({"message": "Access denied."})

        queryset = self.get_queryset()
        serializer = ReadOnlyOrderEntrySerializer(queryset, many=True)

        logger.debug(f"All order entries viewed by {request.user.username}: AllOrderEntriesViewSet API")
        return Response(serializer.data)

    def create(self, request):
        if not request.user.is_staff:
            return Response({"message": "Access denied."})

        created_order_entry = CreationOrderEntrySerializer.create(self=CreationOrderEntrySerializer(), validated_data=request.data)
        created_order_entry.save()

        logger.debug(f"New order entry with id '{created_order_entry.id}' created by {request.user.username} "
                             f"user: AllOrderEntriesViewSet API")
        return Response(request.data)


# Retrieve or update specific order entry
class SpecificOrderEntryViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    def get_order_entry(self, order_entry_id):
        return OrderEntry.objects.filter(id=order_entry_id).first()

    def retrieve(self, request, order_entry_id):
        order_entry = self.get_order_entry(order_entry_id=order_entry_id)
        if order_entry:
            serializer = ReadOnlyOrderEntrySerializer(order_entry)

            logger.debug(f"Book with id {order_entry_id} viewed: SpecificOrderEntryViewSet API")
            return Response(serializer.data)
        else:
            return Response({"message": "Order entry not found."}, status=404)

    def update(self, request, order_entry_id):
        if not request.user.is_staff:
            return Response({"message": "Access denied."})

        order_entry = self.get_order_entry(order_entry_id=order_entry_id)
        if order_entry:
            serializer = CreationOrderEntrySerializer(CreationOrderEntrySerializer.update(self=CreationOrderEntrySerializer(),
                                                                              instance=order_entry, validated_data=request.data))
            logger.debug(f"Book with id {order_entry_id} updated by {request.user.username} user: SpecificBookViewSet API")
            return Response(serializer.data)

        else:
            return Response({"message": "Book to update not found."}, status=404)


# Create, retrieve and update OrderedBook entry
class OrderedBookAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, ordered_book_id):
        ordered_book = OrderedBook.objects.filter(id=ordered_book_id).first()
        if ordered_book:
            serializer = OrderedBookSerializer(ordered_book)
            logger.debug(f"Ordered book entry viewed by {request.user.username} user: OrderedBookAPIView API")
            return Response(serializer.data)
        else:
            return Response({"message": "Ordered book entry not found."}, status=404)

    def post(self, request):
        created_ordered_book = OrderedBookSerializer.create(self=OrderedBookSerializer(), validated_data=request.data)
        created_ordered_book.save()

        logger.debug(f"New ordered book entry with id '{created_ordered_book.id}' created by {request.user.username}"
                     f"user: OrderedBookAPIView API")
        return Response(request.data)

    def put(self, request, ordered_book_id):
        ordered_book = OrderedBook.objects.filter(id=ordered_book_id).first()
        if ordered_book:
            serializer = OrderedBookSerializer(
                OrderedBookSerializer.update(self=OrderedBookSerializer(),
                                                    instance=ordered_book, validated_data=request.data))
            logger.debug(
                f"Ordered book entry with id {ordered_book_id} updated by {request.user.username} user: OrderedBookAPIView API")
            return Response(serializer.data)
