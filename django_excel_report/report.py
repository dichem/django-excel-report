from typing import Iterable, Any

from django.db.models import QuerySet, Model

from .writer import ReportMeta, Writer
from .error import ReportError


class BaseReport(metaclass=ReportMeta):
    model: Model = None
    fields: str | Iterable[str] | dict[str, Any] = None
    # annotations: dict = None

    # next attrs builds in ReportMeta
    _prefetch_related: set[str]
    _select_related: set[str]

    def __init__(self, queryset: QuerySet[Model]):
        if not (queryset.model is self.model):
            raise ReportError("%s class built for model %s, not for %s" % (self.__class__, self.model, queryset.model))
        self.queryset = queryset

    def get_queryset(self) -> QuerySet[Model]:
        # annotations do not ready yet
        return self.queryset.select_related(*self._select_related).prefetch_related(*self._prefetch_related)

    def generate(self):
        writer = Writer("report")
        writer.write_row([[field] for field in self.fields])
        for obj in self:
            writer.write_row(obj)
        writer.wrap()
        writer.save()

    def __iter__(self):
        for obj in self.get_queryset():
            yield self._get_row(obj)

    def _get_row(self, obj: Model) -> list[str | list]:
        return [getattr(self, f'get_{field}')(obj) for field in self.fields]
