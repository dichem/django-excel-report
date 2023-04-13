from typing import Iterable, Type

from django.db import models
from django.db.models.fields.related_descriptors import (
    ManyToManyDescriptor,
    ReverseManyToOneDescriptor,

    ForwardManyToOneDescriptor,
    ReverseOneToOneDescriptor,
    ForwardOneToOneDescriptor
)

from ..error import ReportError

PREFETCH_DESCRIPTORS_ATTRS = {
    ReverseManyToOneDescriptor: lambda x: x.rel.related_model,
    ManyToManyDescriptor: lambda x: x.rel.model
}
TO_SQL_JOIN_DESCRIPTORS = {
    ForwardManyToOneDescriptor: lambda x: x.field.related_model,
    ReverseOneToOneDescriptor: lambda x: x.related.related_model,
    ForwardOneToOneDescriptor: lambda x: x.field.related_model
}


def parse_relations(fields: Iterable[str], model: Type[models.Model]) -> tuple[dict[str, list], dict[str, list]]:
    """Проходится по полям, составляя словари с названиями связанных объектов для join и требуемыми полями"""
    prefetch_related_fields = {}
    select_related_fields = {}

    for field in fields:
        try_field: str
        parsed_field = field.split('__')
        relation, related_field, prefetch_condition = "", "", 0
        next_model = model
        while parsed_field:
            try_field = parsed_field.pop(0)
            descriptor = getattr(next_model, try_field, None)
            if isinstance(descriptor, tuple(PREFETCH_DESCRIPTORS_ATTRS.keys())):
                prefetch_condition = 1
                next_model = PREFETCH_DESCRIPTORS_ATTRS[type(descriptor)](descriptor)
            elif isinstance(descriptor, tuple(TO_SQL_JOIN_DESCRIPTORS.keys())):
                next_model = TO_SQL_JOIN_DESCRIPTORS[type(descriptor)](descriptor)
            else:
                related_field = try_field
                break

            relation += "__%s" % try_field

        if not relation:
            continue

        if not related_field:
            try:
                try_field
            except NameError:
                try_field = ""

            raise ReportError("Не удаётся найти поле '%s' в связанном объекте. Быть может, "
                              "если вы имели ввиду модель %s, необходимо указать конкретное поле "
                              "(%s__name_of_field)" % (try_field, next_model, field))

        try:
            if prefetch_condition:
                prefetch_related_fields[relation.strip('__')].append(related_field)
            else:
                select_related_fields[relation.strip('__')].append(related_field)
        except KeyError:
            if prefetch_condition:
                prefetch_related_fields[relation.strip('__')] = [related_field]
            else:
                select_related_fields[relation.strip('__')] = [related_field]

    return prefetch_related_fields, select_related_fields
