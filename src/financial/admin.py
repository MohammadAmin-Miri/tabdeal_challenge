from django.contrib import admin

from financial.models import Transaction, Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "credit")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = (
        "action",
        "status",
    )
    list_display = (
        "id",
        "wallet",
        "tracking_code",
        "amount",
        "action",
        "status",
    )
