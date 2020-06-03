import uuid

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    category_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    category_uuid = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, "The price must be more than 0.00"),],
    )
    amount = models.PositiveIntegerField()  # available amount

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    finalized = models.BooleanField(default=False)

    @property
    def price(self) -> float:
        """
        :return: Calculated sum of all items multiplied by price
        """
        return sum([item.price_sum for item in self.items.all()])

    def __str__(self):
        return f"Order ID: {self.order_uuid}"


class OrderItem(models.Model):
    order_item_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    class Meta:
        unique_together = ("order", "product")

    @property
    def price_for_one(self) -> float:
        """
        :return: Single product price
        """
        return self.product.price

    @property
    def price_sum(self) -> float:
        """
        :return: Price of all the same products within given order
        """
        return self.product.price * self.amount

    def __str__(self):
        return f"{self.product} ({self.amount} items)"
