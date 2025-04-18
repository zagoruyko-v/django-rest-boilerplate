from django.urls import path
from .views import SendPhoneVerificationCodeView, PhoneAuthView

urlpatterns = [
    path(
        "auth/send-code/",
        SendPhoneVerificationCodeView.as_view(),
        name="send-phone-code",
    ),
    path("auth/verify/", PhoneAuthView.as_view(), name="verify-phone"),
]
