from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import PhoneAuthRequestCodeView, PhoneAuthVerifyCodeView

app_name = "users"

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
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
]
