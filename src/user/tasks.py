from celery import shared_task
from django.db import transaction

from financial.models import Transaction
from .models import PhoneCharge, Seller


@shared_task
@transaction.atomic
def create_phone_charge(tracking_code: str, amount: int, phone: str, seller_id: int):
    seller = Seller.objects.get(id=seller_id)
    wallet = seller.user.wallet
    if amount > wallet.credit:
        return
    transaction = Transaction.objects.create(
        wallet=wallet,
        amount=amount,
        status=Transaction.StatusChoices.SUCCESS,
        action=Transaction.ActionChoices.DECREASE,
    )
    PhoneCharge.objects.create(
        seller=seller,
        transaction=transaction,
        amount=amount,
        phone=phone,
        tracking_code=tracking_code,
        status=PhoneCharge.StatusChoices.SUCCESS,
    )
    wallet.credit -= amount
    wallet.save()
