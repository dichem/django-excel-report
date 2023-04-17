try:
    import django
except ImportError:
    raise ImportError("django-excel-report extension requires django!")

from .report import BaseReport, ReportError
