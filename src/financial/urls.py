from django.urls import path

from .views import IncreaseWalletCreditAPIView

urlpatterns = [
    path(
        "increase/",
        IncreaseWalletCreditAPIView.as_view(),
        name="increase-wallet-credit",
    ),
]
