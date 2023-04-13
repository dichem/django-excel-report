from typing import Iterable, Any

import django.db.models
from django.db.models import QuerySet, Model

from src.django_excel_report.writer import ReportMeta
from .error import ReportError


class BaseReport(metaclass=ReportMeta):
    model: Model = None
    fields: str | Iterable[str] | dict[str, Any] = None
    annotations = None

    # next attrs builds in ReportMeta
    _prefetch_related: set[str]
    _select_related: set[str]

    def __init__(self, queryset: QuerySet[Model]):
        if not (queryset.model is self.model):
            raise ReportError("%s class built for model %s, not for %s" % self.__class__, self.model, queryset.model)
        self.queryset = queryset

    def get_row(self, obj: Model):
        row = []
        for field in self.fields:
            try_related = '__'.join(field.split('__')[:-1])
            if try_related in self._prefetch_related:
                pass
