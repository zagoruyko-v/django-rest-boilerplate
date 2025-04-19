from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    PhoneAuthRequestCodeView,
    PhoneAuthVerifyCodeView,
    UserInfoView,
    UserLogoutView,
)

app_name = "users"

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/logout/", UserLogoutView.as_view(), name="token_logout"),
    path(
        "auth/phone/request/",
        PhoneAuthRequestCodeView.as_view(),
        name="auth_phone_request",
    ),
    path(
        "auth/phone/verify/",
        PhoneAuthVerifyCodeView.as_view(),
        name="auth_phone_verify",
    ),
    path(
        "info/",
        UserInfoView.as_view(),
        name="user_info",
    ),
]
