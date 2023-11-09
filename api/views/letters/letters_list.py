from typing import Union

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from django.utils.html import escape


from ..serializers import LetterSerializer
from ...models import Letter, User
from ..common import (
    staff_get_all,
)

from main.utils import (
    cryptograph_text,
    generate_random_hash,
)
from main.settings import BASE_DIR
from main.cache_manager import cache_manager_singleton

LETTER_DIR = f"{BASE_DIR}/database/letters"


def validate_user(data: dict, msg: str) -> Union[Response, None]:
    try:
        # Get on cache
        if cache_manager_singleton.get("username", data["username"]):
            return None
        else:
            user = User.objects.get(**data)
            # Save on cache
            cache_manager_singleton.set("username", user.username)
    except User.DoesNotExist:
        return Response({"detail": msg}, status=HTTP_400_BAD_REQUEST)
    else:
        return None


class LettersListApiView(APIView):
    def get(self, request, *args, **kwargs):
        return staff_get_all(request, Letter, LetterSerializer)

    def post(self, request, *args, **kwargs):
        text_path = generate_random_hash(fast=True)  # path to save letter
        data = {
            "username": request.data.get("username"),
            "date": request.data.get("date"),
            "sender": escape(request.data.get("sender")),
            "text_path": text_path,
            "letter_token": generate_random_hash(fast=True),
        }
        # Validate user username
        user = validate_user({"username": data["username"]}, "Username is not valid")
        # If validate_user return is not None
        if user:
            return user

        serializer = LetterSerializer(data=data)
        if serializer.is_valid():
            # Save the letter
            text = request.data.get("text")
            text = escape(text)
            text = cryptograph_text(text)
            with open(f"{LETTER_DIR}/{text_path}.txt", "w") as file:
                file.write(text)
            serializer.save()
            return Response(
                {"res": "Letter sent successfully"}, status=HTTP_201_CREATED
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
