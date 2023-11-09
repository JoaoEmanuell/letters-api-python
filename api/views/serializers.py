from rest_framework import serializers
from ..models import User, Letter


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "username", "password", "token"]


class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = ["username", "date", "text_path", "sender", "letter_token"]
