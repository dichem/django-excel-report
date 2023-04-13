from typing import Callable, Iterator
from django.db.models import Model


def get_field(field: str) -> Callable:
    def func(self, obj: Model):
        return getattr(obj, field)
    return func


def get_m2m_generator(rel: str, other_func) -> Callable:
    def func(self, obj: Model) -> Iterator[Callable | str]:
        for m2m in getattr(obj, rel).all():
            yield other_func(self, m2m)
    return func


def get_foreign_field(field: str, other_func) -> Callable:
    def func(self, obj: Model) -> Callable:
        return other_func(self, getattr(obj, field))
    return func


class Accessors:
    FIELD = get_field
    M2M = get_m2m_generator
    FK = get_foreign_field
