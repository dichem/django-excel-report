from django.db.models import QuerySet


def get_queryset_builder(select_related, prefetch_related):
    methods = []
    if select_related:
        methods.append('select_related')
    if prefetch_related:
        methods.append('prefetch_related')

    def func(self):
        for method in methods:
            method = getattr(self.queryset, method)
            method()
        return self.queryset

    return func
