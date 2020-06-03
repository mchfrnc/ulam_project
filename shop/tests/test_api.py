from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from shop.models import Category, Product, Order, OrderItem


class TestApi(TestCase):
    def setUp(self):
        self.price1 = 100
        self.price2 = 200
        self.amount1 = 11
        self.amount2 = 22
        user = User()
        category = Category(name="Test 1")
        category.save()
        self.category2 = Category(name="Test 2")
        category.save()
        self.product1 = Product(
            category_uuid=category, name="Product 1", price=self.price1, amount=100
        )
        self.product1.save()
        self.product2 = Product(
            category_uuid=category, name="Product 2", price=self.price2, amount=50
        )
        self.product2.save()
        self.order = Order(user=user)
        self.order_item1 = OrderItem(
            order=self.order, product=self.product1, amount=self.amount1
        )
        self.order_item2 = OrderItem(
            order=self.order, product=self.product2, amount=self.amount2
        )
        self.client = APIClient()

    def test_get_category(self):
        res = self.client.get("/api/categories/")
        self.assertEqual(200, res.status_code)
        self.assertEqual("Test 1", res.data[0]["name"])

    def test_forbidden_methods_category(self):
        res = self.client.post("/api/categories/", {"name": "Test Name"})
        self.assertEqual(405, res.status_code)
        res = self.client.put(
            f"/api/categories/{self.category2.category_uuid}/", {"name": "Test Name"}
        )
        self.assertEqual(405, res.status_code)
        res = self.client.delete(f"/api/categories/{self.category2.category_uuid}/")
        self.assertEqual(405, res.status_code)

    def test_get_products(self):
        res = self.client.get("/api/products/")
        self.assertEqual(200, res.status_code)
        self.assertEqual("Product 1", res.data[0]["name"])
        self.assertEqual("Product 2", res.data[1]["name"])

    def test_forbidden_methods_products(self):
        res = self.client.post("/api/products/", {"name": "Test Name"})
        self.assertEqual(405, res.status_code)
        res = self.client.put(
            f"/api/products/{self.product1.product_uuid}/", {"name": "Test Name"}
        )
        self.assertEqual(405, res.status_code)
        res = self.client.delete(f"/api/products/{self.product1.product_uuid}/")
        self.assertEqual(405, res.status_code)

    def test_get_orders_without_authentication(self):
        res = self.client.get("/api/orders/")
        self.assertEqual(403, res.status_code)

    def test_get_single_order_without_authentication(self):
        order_id = self.order.order_uuid
        res = self.client.get(f"/api/orders/{order_id}/")
        self.assertEqual(403, res.status_code)

    def test_get_orders_for_authenticated_user_only(self):
        user2 = User()
        user2.save()
        order = Order(user=user2)
        order.save()
        order_item1 = OrderItem(order=order, product=self.product1, amount=1)
        order_item1.save()
        self.client.force_authenticate(user=user2)
        res = self.client.get("/api/orders/")
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(res.data))
        self.assertEqual(100, res.data[0]["price"])

    def test_add_order(self):
        payload = {
            "items": [
                {"product": self.product1.product_uuid, "amount": 1},
                {"product": self.product2.product_uuid, "amount": 2},
            ]
        }
        user2 = User()
        user2.save()
        self.client.force_authenticate(user=user2)
        res = self.client.get("/api/orders/")
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, len(res.data))

        res = self.client.post("/api/orders/", data=payload, format="json")
        self.assertEqual(201, res.status_code)
        self.assertEqual(2, len(res.data["items"]))
        self.assertEqual(1, res.data["items"][0]["amount"])
        self.assertEqual(2, res.data["items"][1]["amount"])

    def test_add_order_for_authenticated_only(self):
        payload = {"items": [{"product": self.product1.product_uuid, "amount": 1},]}

        with self.assertRaises(ValueError):
            self.client.post("/api/orders/", data=payload, format="json")

    def test_delete_order(self):
        payload = {
            "items": [
                {"product": self.product1.product_uuid, "amount": 1},
                {"product": self.product2.product_uuid, "amount": 2},
            ]
        }
        user2 = User()
        user2.save()
        self.client.force_authenticate(user=user2)

        res = self.client.post("/api/orders/", data=payload, format="json")
        self.assertEqual(201, res.status_code)
        self.assertEqual(2, len(res.data["items"]))
        order_id = res.data["order_uuid"]

        res = self.client.delete(f"/api/orders/{order_id}/")
        self.assertEqual(204, res.status_code)

        res = self.client.delete(f"/api/orders/{order_id}/")
        self.assertEqual(404, res.status_code)

    def test_update_order(self):
        payload = {
            "items": [
                {"product": self.product1.product_uuid, "amount": 1},
                {"product": self.product2.product_uuid, "amount": 2},
            ]
        }
        user2 = User()
        user2.save()
        self.client.force_authenticate(user=user2)
        res = self.client.post("/api/orders/", data=payload, format="json")
        order_id = res.data["order_uuid"]

        payload["items"][0]["amount"] = 10
        res = self.client.put(f"/api/orders/{order_id}/", data=payload, format="json")
        self.assertEqual(200, res.status_code)
        self.assertEqual(10, res.data["items"][0]["amount"])

    def test_update_new_order(self):
        payload = {"items": [{"product": self.product1.product_uuid, "amount": 1},]}
        user2 = User()
        user2.save()
        self.client.force_authenticate(user=user2)
        self.client.post("/api/orders/", data=payload, format="json")

        payload["items"].append({"product": self.product2.product_uuid, "amount": 2},)
        res = self.client.post(f"/api/orders/", data=payload, format="json")
        self.assertEqual(201, res.status_code)
        self.assertEqual(2, res.data["items"][1]["amount"])
