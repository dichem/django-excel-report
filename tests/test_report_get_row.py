from django.test import TestCase

from django_excel_report import BaseReport
from .models import Product, Size, Pic


class DefaultSettingsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = p = Product.objects.create(name='p1', picture=Pic.objects.create(img='pic1'))
        p.sizes.add(Size.objects.create(name='nopic'))
        p.sizes.add(Size.objects.create(name='pic', picture=Pic.objects.create(img='1')))

        class TestReport(BaseReport):
            model = Product
            fields = ['name', 'picture__img', 'sizes__name', 'sizes__picture__img']

        cls.report_class = TestReport(Product.objects.all())

    def test_find_related_fields(self):
        row = self.report_class._get_row(self.product)
        self.assertListEqual(
            row,
            [['p1'], ['pic1'], ['nopic', 'pic'], ['', '1']]
        )
