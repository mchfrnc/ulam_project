from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from shop.models import Product, Category, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("category_uuid", "name")
        model = Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("product_uuid", "category_uuid", "name", "price", "amount")
        model = Product


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("product", "amount", "price_for_one")
        model = OrderItem


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        fields = ("order_uuid", "items", "price", "order_date", "finalized")
        read_only_fields = ("order_date", "price", "finalized")
        model = Order

    # TODO: add checking current amount of products available - to not get negative number
    def create(self, validated_data):
        """
        Creates a new empty order and adds order items to it. We want to be sure that
        both operations were executed corectly, so transaction.atomic is used.
        """
        order_items = []
        user = validated_data.pop("user")
        order = Order(user=user)

        for item in validated_data.pop("items"):
            product = item.get("product")
            amount = item.get("amount")
            order_items.append(OrderItem(order=order, product=product, amount=amount))

        with transaction.atomic():
            order.save()
            OrderItem.objects.bulk_create(order_items)
        return order

    def update(self, instance, validated_data):
        """
        Update of an order is in fact executing update on order items.
        """
        order_items = OrderItem.objects.filter(order=instance)

        for item in validated_data.pop("items"):
            product = item.get("product")
            amount = item.get("amount")
            order_items.update_or_create(
                product=product,
                defaults={"order": instance, "product": product, "amount": amount},
            )
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)
