from django.test import TestCase

from .models import Pic, Size, Product, Description
from src.django_excel_report.writer.select_related import get_select_related




class SelectRelatedTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pic = Pic.objects.create(img='image_data')
        size = Size.objects.create(name='size_name', picture=pic)
        product = Product.objects.create(name='product_name', picture=pic)
        product.sizes.add(size)
        Description.objects.create(text='description_text', product=product)

    def test_get_select_related(self):
        fields = ['picture', 'sizes', 'description']
        select_related_fields = get_select_related(fields, Product)
        self.assertEqual(select_related_fields, {'picture', 'description'})
        query = Product.objects.select_related(*select_related_fields).first().get_deferred_fields()
        self.assertEqual(query, {'sizes': {}})
        self.assertEqual(len(connection.queries), 1)
        self.assertIn('SELECT', connection.queries[0]['sql'])
        self.assertIn('FROM', connection.queries[0]['sql'])
        self.assertIn('JOIN', connection.queries[0]['sql'])
        self.assertIn('LEFT OUTER', connection.queries[0]['sql'])
        self.assertIn('picture', connection.queries[0]['sql'])
        self.assertIn('description', connection.queries[0]['sql'])
        self.assertNotIn('sizes', connection.queries[0]['sql'])
