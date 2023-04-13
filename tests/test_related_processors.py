from django.test import TestCase

from .models import Product, Size, Pic
from src.django_excel_report.writer.related_processors import parse_relations
from src.django_excel_report.error import ReportError


class DefaultSettingsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        p = Product.objects.create(name='p1', picture=Pic.objects.create(img='pic1'))
        for i in range(5):
            p.sizes.add(Size.objects.create(name=i))

    def test_find_related_fields(self):
        prefetch_related_fields, select_related_fields = parse_relations(
            ['name', 'sizes__name', 'sizes__picture__name', 'description__text'], Product
        )
        self.assertFalse(
            {'sizes', 'sizes__picture'}.difference(set(prefetch_related_fields.keys()))
        )
        self.assertFalse(
            {'description'}.difference(set(select_related_fields.keys()))
        )

    def test_raises_error(self):
        self.assertRaises(
            ReportError,
            parse_relations,
            ['sizes'], Product
        )
        self.assertRaises(
            ReportError,
            parse_relations,
            ['sizes__picture'], Product
        )
        self.assertRaises(
            ReportError,
            parse_relations,
            ['description'], Product
        )
