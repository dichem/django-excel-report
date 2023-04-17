from .acessors_builder import get_report_attributes

from ..error import ReportError


class ReportMeta(type):
    def __new__(cls, name, bases, attrs: dict):
        """наша цель - принять в метаклассе заданные атрибуты (fields, related fields)
        и на основании их построить класс Report, путём добавления в него нужных методов.
        Обработка заданных параметров заключается в оптимизации запроса (prefetch_related, select_related) и
        имплементации методов работы с каждым объектом queryset."""
        if not bases:
            return super().__new__(cls, name, bases, attrs)

        if attrs["model"] is None:
            raise ReportError("define model attr for %s class" % name)
        elif attrs["fields"] is None:
            raise ReportError("define report fields for %s class" % name)
            
        constructed_attrs = get_report_attributes(attrs["fields"], attrs["model"])
        attrs.update(constructed_attrs)

        return super().__new__(cls, name, bases, attrs)
