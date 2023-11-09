from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
)

from ...models import User
from ..common import (
    get_object,
)

from main.cache_manager import cache_manager_singleton


class UsernameApiView(APIView):
    def get(self, request, username, *args, **kwargs) -> Response:
        if cache_manager_singleton.get("username", username):  # Get in the cache
            return Response({"res": True}, status=HTTP_200_OK)
        else:
            user_instance = get_object(User, {"username": username})
            if not user_instance:
                return Response({"res": False}, status=HTTP_200_OK)

        cache_manager_singleton.set("username", username)  # Set in the cache
        return Response({"res": True}, status=HTTP_200_OK)
