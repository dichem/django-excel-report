from typing import Iterable, Type
from django.db import models
from django.db.models.fields.related_descriptors import (
    ReverseManyToOneDescriptor,
    ReverseOneToOneDescriptor,
    ManyToManyDescriptor,
    ForwardManyToOneDescriptor
)

REVERSE_DESCRIPTORS = (
    ReverseManyToOneDescriptor, ReverseOneToOneDescriptor
)
FORWARD_DESCRIPTORS = (
    ManyToManyDescriptor, ForwardManyToOneDescriptor
)


def get_select_related(fields: Iterable[str], model: Type[models.Model]) -> dict:
    select_related_fields = {}

    for field in fields:
        parsed_field = field.split('__')
        select_related_field = ""
        next_model = model
        while parsed_field:
            try_field = parsed_field.pop(0)
            descriptor = getattr(next_model, try_field, None)
            if isinstance(descriptor, REVERSE_DESCRIPTORS):
                related_name = descriptor.related_name or try_field
                select_related_field += related_name
                next_model = descriptor.rel.related_model
            elif isinstance(descriptor, FORWARD_DESCRIPTORS):
                select_related_field += try_field
                next_model = descriptor.field.related_model
            else:
                break
            select_related_field += "__"
        if select_related_field:
            select_related_fields[select_related_field.rstrip("__")] = {}

    return select_related_fields
