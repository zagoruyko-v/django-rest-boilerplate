from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import PhoneAuthRequestCodeView, PhoneAuthVerifyCodeView, UserInfoView

app_name = "users"

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
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
    path(
        "info/",
        UserInfoView.as_view(),
        name="user_info",
    ),
]
