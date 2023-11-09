from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from ...models import User
from ..common import (
    get_object,
    raise_object_not_exist,
)

from main.utils import compare_hash


class UserLoginApiView(APIView):
    def post(self, request, *args, **kwargs) -> Response:
        data = {
            "username": request.data.get("username"),
            "password": request.data.get("password"),
        }

        user_instance = get_object(User, {"username": data["username"]})
        if not user_instance:
            return raise_object_not_exist(User)

        # Validate password
        if compare_hash(data["password"], user_instance.password):
            return Response({"token": user_instance.token}, status=HTTP_200_OK)

        return Response({"res": "Invalid password"}, status=HTTP_400_BAD_REQUEST)
