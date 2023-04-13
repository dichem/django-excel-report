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
    _prefetch_related: dict[str, list]
    _select_related: dict[str, list]

    def __init__(self, queryset: QuerySet[Model]):
        if not (queryset.model is self.model):
            raise ReportError("%s class built for model %s, not for %s" % self.__class__, self.model, queryset.model)
        self.queryset = queryset
