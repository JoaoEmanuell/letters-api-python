from os import remove
from typing import Union

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from cryptography.fernet import InvalidToken

from ..serializers import LetterSerializer
from ...models import Letter, User
from ..common import (
    format_return_data,
)

from main.utils import (
    decrypt_text,
)
from main.settings import BASE_DIR
from main.cache_manager import cache_manager_singleton

LETTER_DIR = f"{BASE_DIR}/database/letters"


def validate_user(data: dict, msg: str) -> Union[Response, None]:
    try:
        user = User.objects.get(**data)
    except User.DoesNotExist:
        return Response({"detail": msg}, status=HTTP_400_BAD_REQUEST)
    else:
        return None


class LetterUserListApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = {
            "username": request.data.get("username"),
            "token": request.data.get("token"),
            "index-init": request.data.get("index-init"),
            "index-end": request.data.get("index-end"),
            "index-all": request.data.get("index-all"),
        }
        # Validate the index
        if (
            data["index-init"] == None
            or data["index-end"] == None
            or type(data["index-init"]) != int
            or type(data["index-end"]) != int
        ):
            data["index-init"] = 0
            data["index-end"] = 20
        else:
            data["index-init"] = int(data["index-init"])
            data["index-end"] = int(data["index-end"])

        # Get on the cache
        cache = cache_manager_singleton.get("letters_user", data["token"])
        if cache:
            return Response(cache, status=HTTP_200_OK)

        user_instance = validate_user(
            {"username": data["username"], "token": data["token"]},
            "Username or token is not valid",
        )
        if user_instance:
            return user_instance

        if not data["index-all"]:
            letters = Letter.objects.order_by("date").filter(username=data["username"])[
                data["index-init"] : data["index-end"]
            ]
        else:
            letters = Letter.objects.order_by("date").filter(
                username=data["username"]
            )  # Index all user letters
        serializer = LetterSerializer(letters, many=True)
        serializer_data = serializer.data

        # Decrypt letter

        for i, letter in enumerate(letters):
            try:
                with open(f"{LETTER_DIR}/{letter.text_path}.txt", "r") as file:
                    try:
                        text = decrypt_text(file.read())
                    except InvalidToken:  # If letter is empty
                        text = ""
            except FileNotFoundError:
                text = ""
            serializer_data[i]["text"] = text

        return_data = format_return_data(
            list(serializer_data),
            include_fields=["date", "sender", "text", "letter_token"],
        )
        # Set on the cache
        cache_manager_singleton.set(
            "letters_user", {"user_token": data["token"], "letters": return_data}
        )

        return Response(return_data, status=HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        data = {
            "username": request.data.get("username"),
            "token": request.data.get("token"),
        }

        user_instance = validate_user(data, "Username or token is not valid")
        if user_instance:
            return user_instance
        else:
            letters = Letter.objects.filter(username=data["username"])

            # Remove letter from server

            for letter in letters:
                try:
                    remove(f"{LETTER_DIR}/{letter.text_path}.txt")
                except FileNotFoundError:
                    pass

            # Delete from database

            letters.delete()

            # Remove from cache

            cache_manager_singleton.delete("letters_user", data["token"])

            return Response({"res": "Letters deleted!"}, status=HTTP_200_OK)
