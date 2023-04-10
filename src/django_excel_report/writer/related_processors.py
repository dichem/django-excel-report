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


def get_prefetch_related(fields: Iterable[str], model: Type[models.Model]):
    """Проходится по полям, составляя список полей для prefetch_related"""
    prefetch_related_fields = set()

    for field in fields:
        parsed_field = field.split('__')
        prefetch_related_field = ""
        next_model = model
        while parsed_field:
            try_field = parsed_field.pop(0)
            descriptor = getattr(next_model, try_field, None)
            if isinstance(descriptor, REVERSE_DESCRIPTORS):
                next_model = descriptor.rel.model
            elif isinstance(descriptor, FORWARD_DESCRIPTORS):
                next_model = descriptor.field.related_model
            else:
                break
            prefetch_related_field += "__%s" % try_field

        if prefetch_related_field:
            prefetch_related_fields.add(prefetch_related_field.strip('__'))

    return prefetch_related_fields
