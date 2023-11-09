from typing import Union

from django.db.models import Model
from django.utils.html import escape
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK,
)
from rest_framework.serializers import ModelSerializer
from rest_framework.request import Request


def get_object(model: Model, data: dict) -> Union[Model, None]:
    """Get object or none if not exists

    Args:
        model (Model): Model created on models
        data (dict): Data for search

    Returns:
        Union[Model, None]: If exists data, return it, else, return None
    """
    try:
        return model.objects.get(**data)
    except model.DoesNotExist:
        return None


def raise_object_not_exist(model: Model) -> Response:
    """Return a response if object don't exists

    Args:
        model (Model): Model created on models

    Returns:
        Response: Response with dict, and status 400
    """
    return Response(
        {"res": f"{model._meta.model_name.capitalize()} don't exists"},
        status=HTTP_400_BAD_REQUEST,
    )


def optional_fields(
    object_instance: Model, data: dict, optional_fields: list[str]
) -> dict:
    """If field don't passed on request, use the original value saved in database

    Args:
        object_instance (Model): Object instance saved in the database
        data (dict): Data with the request dict
        optional_fields (list[str]): optional fields for validate

    Returns:
        dict: _description_
    """
    new_data = {}

    for field in optional_fields:
        value = data.get(field)
        if not value:
            new_data[field] = object_instance.__getattribute__(
                field
            )  # Original value saved
            new_data[f"_{field}_data"] = object_instance.__getattribute__(field)
        else:
            new_data[field] = escape(value)
            new_data[f"_{field}_data"] = escape(value)

    return new_data


def format_return_data(
    data: Union[dict, list[dict]] = {},
    include_fields: list[str] = [],
    exclude_fields: list[str] = [],
) -> dict:
    """Format the return data

    Args:
        data (dict, optional): Data to format. Defaults to {}.
        include_fields (list[str], optional): Include fields, if field is added, this field is returned, others fields is ignored. Defaults to [].
        exclude_fields (list[str], optional): Exclude fields, if field is added, this field is excluded, others fields is returned. Defaults to [].

    Returns:
        dict: dict with data validated
    """
    # List
    new_data = []
    if type(data) == list:
        for _dict in data:
            new_data.append(_format_dict(_dict, include_fields, exclude_fields))
        return new_data
    # Simple dict
    else:
        return _format_dict(data, include_fields, exclude_fields)


def _format_dict(
    data: dict = {}, include_fields: list[str] = [], exclude_fields: list[str] = []
) -> dict:
    """Format the dict data

    Args:
        data (dict, optional): Data to format. Defaults to {}.
        include_fields (list[str], optional): Include fields, if field is added, this field is returned, others fields is ignored. Defaults to [].
        exclude_fields (list[str], optional): Exclude fields, if field is added, this field is excluded, others fields is returned. Defaults to [].

    Returns:
        dict: dict with data validated
    """
    if include_fields != []:
        new_data = {}
        for field in include_fields:
            new_data[field] = data.get(field)
        return new_data
    elif exclude_fields != []:
        new_data = data.copy()
        for field in exclude_fields:
            new_data.pop(field)
        return new_data
    else:
        return {}


def staff_get_all(request: Request, model: Model, serializer: ModelSerializer):
    """Get all data from model if user is staff

    Args:
        request (Request): Request from view, to verify if user is staff
        model (Model): Model to get data
        serializer (ModelSerializer): Model serializer to serializer data

    Returns:
        Response: Return a response with data if user is staff or detail if user not staff
    """
    if request.user.is_staff:  # Validate if user is staff
        data = model.objects.all()
        serialized = serializer(data, many=True)
        return Response(serialized.data, status=HTTP_200_OK)
    return Response(
        {"detail": "Authentication credentials were not provided."},
        status=HTTP_401_UNAUTHORIZED,
    )
