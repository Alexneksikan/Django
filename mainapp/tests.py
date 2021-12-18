from django.test import TestCase
from mainapp.models import ProductCategory, Product
from django.test.client import Client


class TestMainappSmoke(TestCase):
    status_ok = 200
    status_redirect = 302

    def setUp(self) -> None:
        self.category = ProductCategory.objects.create(
            name='cat1'
        )
        for i in range(10):
            Product.objects.create(
                name=f'prod-{i}',
                category=self.category,
                short_desc='shortdesc',
                description='desc'
            )
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, self.status_ok)

    def test_products_urls(self):
        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, self.status_ok)

    def test_categories_urls(self):
        for cat in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{cat.pk}/')
            self.assertEqual(response.status_code, self.status_ok)


class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name="стулья")
        self.product_1 = Product.objects.create(name="стул 1",
                                          category=category,
                                          price=1999.5,
                                          quantity=150)

        self.product_2 = Product.objects.create(name="стул 2",
                                          category=category,
                                          price=2998.1,
                                          quantity=125,
                                          is_active=False)

        self.product_3 = Product.objects.create(name="стул 3",
                                          category=category,
                                          price=998.1,
                                          quantity=115)

    def test_product_get(self):
        product_1 = Product.objects.get(name="стул 1")
        product_2 = Product.objects.get(name="стул 2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(name="стул 1")
        product_2 = Product.objects.get(name="стул 2")
        self.assertEqual(str(product_1), 'стул 1 (стулья)')
        self.assertEqual(str(product_2), 'стул 2 (стулья)')

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="стул 1")
        product_3 = Product.objects.get(name="стул 3")
        products = product_1.get_items()

        self.assertEqual(list(products), [product_1, product_3])
