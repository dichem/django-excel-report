from django.test import TestCase

from .models import Product, Size, Pic
from src.django_excel_report.report import BaseReport


class DefaultSettingsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        p = Product.objects.create(name='p1', picture=Pic.objects.create(img='pic1'))
        for i in range(5):
            p.sizes.add(Size.objects.create(name=i))

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        class ReportClass(BaseReport):
            model = Product
            fields = ['name', 'sizes__name', 'sizes__picture__name', 'description__text']
        cls.report_class = ReportClass

        class EmptyRelatedClass(BaseReport):
            model = Product
            fields = ['name', 'pk']
        cls.empty_related_class = EmptyRelatedClass

    def test_has_prefetch_related(self):
        self.assertIsNotNone(self.report_class._prefetch_related)
        self.assertIsNotNone(self.report_class._select_related)

    def test_has_empty_dicts(self):
        self.assertDictEqual(self.empty_related_class._prefetch_related, {})
        self.assertDictEqual(self.empty_related_class._select_related, {})
