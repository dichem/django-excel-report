from typing import Iterable, Any

import django.db.models
from django.db.models import QuerySet, Model

from src.django_excel_report.writer import ReportMeta, ReportError


class BaseReport(metaclass=ReportMeta):
    model: Model = None
    fields: str | Iterable[str] | dict[str, Any] = None
    annotations = None

    def __init__(self, queryset: QuerySet[Model]):
        if not (queryset.model is self.model):
            raise ReportError("%s class built fot model %s, not for %s" % self.__class__, self.model, queryset.model)
        self.queryset = queryset


class Rep(BaseReport):
    model = 1


class R(Rep):
    model = None


if __name__ == "__main__":
    print(Rep.a)
