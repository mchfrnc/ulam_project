from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urls = [
    path("obtain_token/", TokenObtainPairView.as_view(), name="obtain_token"),
    path("refresh_token/", TokenRefreshView.as_view(), name="refresh_token"),
]
