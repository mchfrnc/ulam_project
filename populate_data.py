import random

from shop.models import Category, Product

categories = ["Computers", "Fruits", "T-shirts", "Flowers", "Bikes", "Books", "Cars", "Houses"]


def populate_category():
    for c in categories:
        Category.objects.update_or_create(name=c)
    return Category.objects.all()


def populate_product(categories):
    products = ["Item", "Product", "Thing", "Element"]

    for c in categories:
        for p in products:
            Product.objects.update_or_create(
                category_uuid=c,
                name=p,
                price=random.randint(1, 100),
                amount=random.randint(1, 100),
            )
    return Product.objects.all()


def run():
    new_categories = populate_category()
    new_products = populate_product(new_categories)
