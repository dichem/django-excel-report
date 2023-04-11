from django.test import TestCase

from .models import Product, Size
from src.django_excel_report.writer.related_processors import get_prefetch_related


class DefaultSettingsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        p = Product.objects.create(name='p1')
        for i in range(5):
            p.sizes.add(Size.objects.create(name=i))

    def test_find_related_fields(self):
        prefetch_related_fields = get_prefetch_related(
            ['sizes', 'name', 'sizes__picture', 'sizes__name', 'sizes__picture__name'], Product
        )
        self.assertFalse(
            {'sizes', 'sizes__picture'}.difference(prefetch_related_fields)
        )
