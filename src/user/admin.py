from django.contrib import admin

from .models import Seller, PhoneCharge


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
    )


@admin.register(PhoneCharge)
class PhoneChargeAdmin(admin.ModelAdmin):
    list_filter = ("seller", "phone")
    list_display = (
        "id",
        "seller",
        "phone",
        "transaction",
        "amount",
        "status",
    )
