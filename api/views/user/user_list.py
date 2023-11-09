from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from django.utils.html import escape

from ..serializers import UserSerializer
from ...models import User
from ..common import (
    staff_get_all,
)

from main.utils import generate_hash, generate_random_hash
from main.cache_manager import cache_manager_singleton


class UserListApiView(APIView):
    def get(self, request, *args, **kwargs):  # Get all users, some staff
        return staff_get_all(request, User, UserSerializer)

    def post(self, request, *args, **kwargs):  # Register user
        # Verify if username exists in cache
        if cache_manager_singleton.get("username", request.data.get("username")):
            return Response(
                {"username": ["user with this username already exists."]},
                status=HTTP_400_BAD_REQUEST,
            )

        token = generate_random_hash()
        data = {
            "name": escape(request.data.get("name")),
            "username": escape(request.data.get("username")),
            "password": generate_hash(request.data.get("password")),
            "token": token,
        }

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # Save username in cache
            cache_manager_singleton.set("username", data["username"])
            return Response(
                {"token": serializer.data["token"]}, status=HTTP_201_CREATED
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
