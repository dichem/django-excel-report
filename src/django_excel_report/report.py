from typing import Iterable

import django.db.models
from django.db.models import QuerySet, Model

from .writer import ReportWriter


class BaseReport(metaclass=ReportWriter):
    fields: str | Iterable[str] = None
    annotations = None

    def __init__(self, queryset: QuerySet[Model]):
        self.queryset = queryset
        self.writer = self.__class__.__class__
        if isinstance(self.fields, str):
            self.fields = (self.fields, )
        
    def generate(self):
        pass

    def get_queryset(self):
        return self.queryset


class ForeignRelationReportMixin:
    pass


class InverseRelationReportMixin:
    pass


class M2mRelationReportMixin:
    pass


if __name__ == "__main__":
    BaseReport('a')
django.db.models.Model