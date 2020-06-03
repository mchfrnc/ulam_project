from unittest import skip

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from shop.models import Category, Product, Order, OrderItem


class TestFailed(Exception):
    pass


class TestProduct(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name="Example Category")

    def test_minimum_price(self):
        try:
            Product.objects.create(
                category_uuid=self.category1, name="Product1", price=-10.00, amount=12
            )
        except ValidationError as e:
            # to indicate the exact validation problem, not any problem
            self.assertIn("price", e.error_dict.keys())
            self.assertEqual(1, len(e.error_dict.keys()))
        else:
            raise TestFailed()

    def test_minimum_amount(self):
        try:
            Product.objects.create(
                category_uuid=self.category1, name="Product1", price=10.00, amount=-1
            )
        except ValidationError as e:
            # to indicate the exact validation problem, not any problem
            self.assertIn("amount", e.error_dict.keys())
            self.assertEqual(1, len(e.error_dict.keys()))
        else:
            raise TestFailed()


class TestOrders(TestCase):
    def setUp(self):
        self.price1 = 100
        self.price2 = 200
        self.amount1 = 11
        self.amount2 = 22
        user = User()
        category = Category("Test 1")
        self.product1 = Product(category, "Product 1", price=self.price1, amount=100)
        product2 = Product(category, "Product 2", price=self.price2, amount=50)
        self.order = Order(user=user)
        self.order_item1 = OrderItem(
            order=self.order, product=self.product1, amount=self.amount1
        )
        self.order_item2 = OrderItem(
            order=self.order, product=product2, amount=self.amount2
        )

    def test_price_for_one_in_order_item(self):
        self.assertEqual(self.product1.price, self.order_item1.price_for_one)

    def test_price_sum_in_order_item(self):
        expected_sum = self.price1 * self.amount1
        self.assertEqual(expected_sum, self.order_item1.price_sum)

    @skip("Needs to be fixed")
    def test_price_in_order(self):
        expected_sum = self.price1 * self.amount1 + self.price2 * self.amount2
        self.assertEqual(expected_sum, self.order.price)

    def test_new_order_not_finalized(self):
        self.assertEqual(self.order.finalized, False)
