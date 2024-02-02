import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


user_model = get_user_model()


class Wallet(models.Model):

    user = models.OneToOneField(
        user_model, on_delete=models.CASCADE, related_name="wallet"
    )
    credit = models.PositiveBigIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "user",
                ]
            ),
        ]


class Transaction(models.Model):

    class ActionChoices(models.TextChoices):
        INCREASE = "increase", _("Increase")
        DECREASE = "decrease", _("Decrease")

    class ResultChoices(models.TextChoices):
        SUCCESS = "success", _("Success")
        FAILURE = "failure", _("Failure")
        PENDING = "pending", _("Pending")

    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="transactions"
    )
    tracking_code = models.UUIDField(default=uuid.uuid4, editable=False)
    action = models.CharField(
        max_length=16, choices=ActionChoices, default=ActionChoices.INCREASE
    )
    result = models.CharField(
        max_length=16, choices=ResultChoices, default=ResultChoices.PENDING
    )
    amount = models.PositiveBigIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "tracking_code",
                ]
            ),
            models.Index(
                fields=[
                    "action",
                ]
            ),
        ]
