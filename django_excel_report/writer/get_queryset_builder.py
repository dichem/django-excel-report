from typing import Iterable, Callable

from django.db.models import QuerySet, Model


def get_queryset_builder(
    select_related: Iterable[str], prefetch_related: Iterable[str], annotate_fields: dict
) -> Callable:
    def get_queryset(self) -> QuerySet[Model]:
        return self.queryset

    if select_related:
        def select_related_decorator(func: Callable) -> Callable:
            def wrapper(self) -> QuerySet[Model]:
                return func(self).select_related(*select_related)

            return wrapper

        get_queryset = select_related_decorator(get_queryset)

    if prefetch_related:
        def prefetch_related_decorator(func: Callable) -> Callable:
            def wrapper(self) -> QuerySet[Model]:
                return func(self).prefetch_related(*prefetch_related)

            return wrapper

        get_queryset = prefetch_related_decorator(get_queryset)

    if annotate_fields:
        def annotate_decorator(func: Callable):
            def wrapper(self) -> QuerySet[Model]:
                return func(self).annotate(**annotate_fields)

            return wrapper

        get_queryset = annotate_decorator(get_queryset)

    return get_queryset
