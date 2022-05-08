import json

from django.contrib import auth
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from user.models import BookstoreUser
from user.serializers import DetailedUserSerializer

import logging

logger = logging.getLogger(__name__)


# Allows to view user account
# class BookstoreUserReadOnlyAPIView(APIView):
#     permission_classes = (IsAdminUser,)
#
#     def get(self, request, user_id):
#         user = BookstoreUser.objects.filter(id=user_id).first()
#
#         if user:
#             serializer = DetailedUserSerializer(user)
#             logger.debug(f"User with id {user_id} viewed by {request.user.username} user: BookstoreUserReadOnlyAPIView API")
#             return Response(serializer.data)
#         else:
#             return Response({"message": "User not found."}, status=404)


# Login through username and password
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            logger.debug(f"User {username} successfully logged in")
            return Response({"message": "User " + username + " successfully logged in."})
        else:
            logger.debug(f"A problem occured while logging in with username {username}")
            return Response({"message": "A problem occured while logging in. Try different username or password."})


# Create new user through console
def create_user(username, password, email):
    user_model = get_user_model()
    user = user_model.objects.create_user(username=username, password=password)
    user.email = email

    user.is_superuser = False
    user.is_staff = False

    user.save()