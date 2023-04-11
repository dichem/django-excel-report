import django.db.models
import xlsxwriter


class ReportError(Exception):
    pass


class ReportMeta(type):
    def __new__(cls, name, bases, attrs):
        """наша цель - принять в метаклассе заданные атрибуты (fields, related fields)
        и на основании их построить класс Report, путём добавления в него нужных методов.
        Обработка заданных параметров заключается в оптимизации запроса (prefetch_related, select_related) и
        имплементации методов работы с каждым объектом queryset."""
        if not bases:
            return super().__new__(cls, name, bases, attrs)
        if attrs["model"] is None:
            raise ReportError("define model attr for %s class" % name)

        attrs["preferch_related"] = get_prefetch_relater(attrs["model"], attrs["prefetch_related"])

        attrs["a"] = 'aaaa'
        return super().__new__(cls, name, bases, attrs)
