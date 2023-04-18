from typing import Callable, Iterator, Generator

from django.db.models import Model


def get_field(field: str) -> Callable:
    def func(self, obj: Model, from_iterator=False):
        if from_iterator:
            return getattr(obj, field, "")
        return [getattr(obj, field, "")]
    return func


def get_m2m_generator(rel: str, other_func) -> Callable:
    def func(self, obj: Model, from_iterator=False) -> Iterator[Callable | str]:
        for m2m_obj in getattr(obj, rel).all():
            yield other_func(self, m2m_obj, from_iterator=True)
    return func


def get_foreign_field(field: str, other_func) -> Callable:
    def func(self, obj: Model, from_iterator=False) -> Callable:
        # if fk is null, get_field anyway returns empty string
        return other_func(self, getattr(obj, field, ""), from_iterator)
    return func


def get_values_list(func):
    def wrapper(self, obj=None, result=None, recursive_call=False):
        values_list = []
        if obj:
            result = func(self, obj)

        if not isinstance(result, (list, Generator)):
            if result is not None:
                values_list.append(str(result))

        else:
            for entity in result:
                if not isinstance(entity, (list, Generator)) and entity is not None:
                    values_list.append(str(entity))
                else:
                    values_list.extend(wrapper(self, result=entity, recursive_call=True))
        if recursive_call:
            return values_list
        return values_list or [""]

    return wrapper


class Accessors:
    FIELD = get_field
    M2M = get_m2m_generator
    FK = get_foreign_field
    GET_VALUES_LIST = get_values_list
