from django.test import TestCase
from product.models import Product  # Adjust import path if needed

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            code='1 or 2A',
            product_description='Test Product Description',
            weight_kg=2.5
        )

    def test_code_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('code').verbose_name
        self.assertEqual(field_label, 'code')

    def test_product_description_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('product_description').verbose_name
        self.assertEqual(field_label, 'product description')

    def test_weight_kg_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('weight_kg').verbose_name
        self.assertEqual(field_label, 'weight kg')

    def test_code_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('code').max_length
        self.assertEqual(max_length, 10)

    def test_product_description_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('product_description').max_length
        self.assertEqual(max_length, 100)

    def test_object_str_is_code(self):
        product = Product.objects.get(id=1)
        self.assertEqual(str(product), product.code)
