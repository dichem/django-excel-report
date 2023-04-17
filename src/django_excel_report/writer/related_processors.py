from typing import Iterable, Type, Callable

from django.db import models
from django.db.models.query_utils import DeferredAttribute
from django.db.models.fields.related_descriptors import (
    ManyToManyDescriptor,
    ReverseManyToOneDescriptor,

    ForwardManyToOneDescriptor,
    ReverseOneToOneDescriptor,
    ForwardOneToOneDescriptor
)

from ..error import ReportError
from .accessors import Accessors

PREFETCH_DESCRIPTORS_ATTRS = {
    ReverseManyToOneDescriptor: lambda x: x.rel.related_model,
    ManyToManyDescriptor: lambda x: x.rel.model
}
TO_SQL_JOIN_DESCRIPTORS = {
    ForwardManyToOneDescriptor: lambda x: x.field.related_model,
    ReverseOneToOneDescriptor: lambda x: x.related.related_model,
    ForwardOneToOneDescriptor: lambda x: x.field.related_model
}


def get_report_attributes(fields: Iterable[str], model: Type[models.Model]) -> dict[str, Callable | set]:
    """Проходится по полям, составляя словари с названиями связанных объектов для join и требуемыми полями"""
    prefetch_related_fields = set()
    select_related_fields = set()
    attributes = {}

    for field in fields:
        parsed_field = field.split('__')
        relation, prefetch_condition = "", 0
        related_field = try_field = ""
        current_model = model
        reverse_access_methods = []
        while parsed_field:
            try_field = parsed_field.pop(0)
            descriptor = getattr(current_model, try_field, None)
            if isinstance(descriptor, tuple(PREFETCH_DESCRIPTORS_ATTRS.keys())):
                prefetch_condition = 1
                current_model = PREFETCH_DESCRIPTORS_ATTRS[type(descriptor)](descriptor)

                reverse_access_methods.append({'field': try_field, 'method': Accessors.M2M})

            elif isinstance(descriptor, tuple(TO_SQL_JOIN_DESCRIPTORS.keys())):
                current_model = TO_SQL_JOIN_DESCRIPTORS[type(descriptor)](descriptor)

                reverse_access_methods.append({'field': try_field, 'method': Accessors.FK})

            elif isinstance(descriptor, (DeferredAttribute, property)):
                related_field = try_field
                reverse_access_methods.append({'field': try_field, 'method': Accessors.FIELD})
                if not parsed_field:
                    break
                else:
                    raise ReportError("Поле %s модели %s не имеет связи к %s" %
                                      (related_field, current_model, parsed_field.pop(0)))

            elif descriptor is None:
                getattr(current_model, try_field)

            else:
                raise ReportError("Неправильно указано поле %s" % field)

            relation += "__%s" % try_field

        if not related_field:
            raise ReportError("Не удаётся найти поле '%s' в связанном объекте. Быть может, "
                              "если вы имели ввиду модель %s, необходимо указать конкретное поле "
                              "(%s__name_of_field)" % (try_field, current_model, field))

        if prefetch_condition and relation:
            prefetch_related_fields.add(relation.strip('__'))
        elif relation:
            select_related_fields.add(relation.strip('__'))

        field_accessor_data = reverse_access_methods.pop()
        field_accessor = field_accessor_data['method'](field_accessor_data['field'])
        for data in reverse_access_methods[::-1]:
            field_accessor = data['method'](data['field'], field_accessor)

        attributes[f"get_{field}"] = Accessors.GET_VALUES_LIST(field_accessor)

    attributes["_prefetch_related"] = prefetch_related_fields
    attributes["_select_related"] = select_related_fields

    return attributes
