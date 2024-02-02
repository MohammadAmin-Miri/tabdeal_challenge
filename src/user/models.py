import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from financial.models import Transaction


user_model = get_user_model()


class Seller(models.Model):

    user = models.OneToOneField(
        user_model, on_delete=models.CASCADE, related_name="seller"
    )
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


class PhoneCharge(models.Model):

    class StatusChoices(models.TextChoices):
        SUCCESS = "success", _("Success")
        FAILURE = "failure", _("Failure")
        PENDING = "pending", _("Pending")

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="charges")
    tracking_code = models.UUIDField(default=uuid.uuid4, editable=False)
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="charge",
        null=True,
        blank=True,
    )
    amount = models.PositiveBigIntegerField(default=0)
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^(\+98|0)?9\d{9}$",
                message="Enter a valid phone number.",
            ),
        ],
    )
    status = models.CharField(
        max_length=16, choices=StatusChoices, default=StatusChoices.PENDING
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "seller",
                ]
            ),
            models.Index(
                fields=[
                    "phone",
                ]
            ),
        ]
