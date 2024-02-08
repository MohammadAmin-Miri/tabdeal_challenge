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

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="charges")
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="charge",
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^(\+98|0)?9\d{9}$",
                message="Enter a valid phone number.",
            ),
        ],
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

    @property
    def amount(self):
        if self.transaction:
            return self.transaction.amount
        return None

    @property
    def status(self):
        if self.transaction:
            return self.transaction.status
        return None
