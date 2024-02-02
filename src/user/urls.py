from django.urls import path

from user.views import ChargeAPIView


urlpatterns = [
    path("charge/", ChargeAPIView.as_view(), name="charge-phone")
]
