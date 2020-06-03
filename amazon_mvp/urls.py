from django.contrib import admin
from django.urls import path, include

from auth.urls import urls as auth_urls
from shop.urls import urls as shop_urls


urlpatterns = [
    path("api/", include(shop_urls)),
    path("api/auth/", include(auth_urls)),
    path("admin/", admin.site.urls),
]
