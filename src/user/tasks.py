from celery import shared_task
from django.db import transaction

from financial.models import Transaction
from .models import PhoneCharge, Seller


@shared_task
@transaction.atomic
def create_phone_charge(charge_id: int, amount: int, tracking_code: str):
    charge = PhoneCharge.objects.select_for_update().get(id=charge_id)
    wallet = charge.seller.user.wallet
    if amount > wallet.credit:
        return

    transaction = Transaction.objects.select_for_update().create(
        wallet=wallet,
        action=Transaction.ActionChoices.DECREASE,
        status=Transaction.StatusChoices.SUCCESS,
        amount=amount,
        tracking_code=tracking_code,
    )
    charge.transaction = transaction
    charge.save()
    wallet.credit -= amount
    wallet.save()
