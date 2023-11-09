from os import remove

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
)

from ..serializers import LetterSerializer
from ...models import Letter
from ..common import (
    get_object,
    raise_object_not_exist,
)

from main.utils import (
    decrypt_text,
)
from main.settings import BASE_DIR

LETTER_DIR = f"{BASE_DIR}/database/letters"


class LetterDetailApiView(APIView):
    def get(self, request, letter_token, *args, **kwargs):
        letter_instance = get_object(Letter, {"letter_token": letter_token})
        if not letter_instance:
            return raise_object_not_exist(Letter)

        serializer = LetterSerializer(letter_instance)
        # Decrypt letter
        serializer_data = serializer.data
        text_path = letter_instance.text_path

        with open(f"{LETTER_DIR}/{text_path}.txt", "r") as file:
            text = file.read()

        text = decrypt_text(text)
        serializer_data["text"] = text

        return Response(serializer_data, status=HTTP_200_OK)

    def delete(self, request, letter_token, *args, **kwargs):
        letter_instance = get_object(Letter, {"letter_token": letter_token})
        if not letter_instance:
            return raise_object_not_exist(Letter)

        letter_instance.delete()
        try:
            remove(f"{LETTER_DIR}/{letter_instance.text_path}.txt")
        except FileNotFoundError:
            pass
        return Response({"res": "Letter deleted!"}, status=HTTP_200_OK)
