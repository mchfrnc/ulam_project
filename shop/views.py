from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from shop.models import Product, Category, Order
from shop.serializers import (
    ProductSerializer,
    CategorySerializer,
    OrderSerializer,
    UserSerializer,
)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# TODO: add possibility to create, update, delete Product and Category only for staff members
# TODO: add possibility to mark order as finalized for staff member only


class IsStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class CategoryViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwner,)
    authentication_class = (JSONWebTokenAuthentication,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        Only authenticated user is allowed to see his transactions.
        """
        user = self.request.user
        if user.is_authenticated:
            return Order.objects.filter(user=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        """
        Every order has to be saved with authenticated user as it's owner.
        """
        serializer.save(user=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    # TODO: make this visible only for authenticated users
    http_method_names = ["get"]
    queryset = User.objects.all()
    serializer_class = UserSerializer
