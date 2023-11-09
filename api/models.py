from django.db import models

# Create your models here.

from encrypted_fields import fields

from main.settings import FIELD_ENCRYPTION_KEYS


class User(models.Model):
    _name_data = fields.EncryptedTextField(max_length=100, default="", null=False)
    name = fields.SearchField(
        hash_key=FIELD_ENCRYPTION_KEYS[0], encrypted_field_name="_name_data"
    )

    _username_data = fields.EncryptedTextField(max_length=50, default="", null=False)
    username = fields.SearchField(
        hash_key=FIELD_ENCRYPTION_KEYS[1],
        encrypted_field_name="_username_data",
        unique=True,
    )

    _password_data = fields.EncryptedTextField(max_length=100, default="", null=False)
    password = fields.SearchField(
        hash_key=FIELD_ENCRYPTION_KEYS[2],
        encrypted_field_name="_password_data",
    )  # hash

    _token_data = fields.EncryptedTextField(
        max_length=100, blank=True, default="", null=True
    )
    token = fields.SearchField(
        hash_key=FIELD_ENCRYPTION_KEYS[3],
        encrypted_field_name="_token_data",
        unique=True,
    )

    class Meta:
        verbose_name_plural = "users"


class Letter(models.Model):
    _username_data = fields.EncryptedTextField(max_length=100, default="", null=False)
    username = fields.SearchField(
        hash_key=FIELD_ENCRYPTION_KEYS[4], encrypted_field_name="_username_data"
    )

    _date_data = fields.EncryptedDateField(max_length=100, auto_now=True, null=False)
    date = fields.SearchField(
        hash_key=FIELD_ENCRYPTION_KEYS[5], encrypted_field_name="_date_data"
    )

    _text_path_data = fields.EncryptedTextField(max_length=100, default="", null=False)
    text_path = fields.SearchField(
        hash_key=FIELD_ENCRYPTION_KEYS[6], encrypted_field_name="_text_path_data"
    )

    _sender_data = fields.EncryptedTextField(max_length=100, default="", null=False)
    sender = fields.SearchField(
        hash_key=FIELD_ENCRYPTION_KEYS[7], encrypted_field_name="_sender_data"
    )

    _letter_token_data = fields.EncryptedTextField(
        max_length=100, default="", null=False
    )
    letter_token = fields.SearchField(
        hash_key=FIELD_ENCRYPTION_KEYS[8], encrypted_field_name="_letter_token_data"
    )

    class Meta:
        verbose_name_plural = "letters"
