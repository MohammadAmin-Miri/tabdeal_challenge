from celery import shared_task
from django.db import transaction

from financial.models import Transaction
from .models import PhoneCharge, Seller


@shared_task
@transaction.atomic
def create_phone_charge(charge_id: int):
    charge = PhoneCharge.objects.get(id=charge_id)
    wallet = charge.seller.user.wallet
    if charge.amount > wallet.credit:
        return

    Transaction.objects.create(
        wallet=wallet,
        action=Transaction.ActionChoices.DECREASE,
        status=Transaction.StatusChoices.SUCCESS,
        amount=charge.amount,
    )
    charge.status = PhoneCharge.StatusChoices.SUCCESS
    charge.save()
    wallet.credit -= charge.amount
    wallet.save()
