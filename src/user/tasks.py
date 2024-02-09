from datetime import timedelta
from celery import shared_task
from django.db import OperationalError, transaction

from financial.models import Transaction
from .models import PhoneCharge, Seller


@shared_task(
    bind=True,
    autoretry_for=(OperationalError,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 20},
)
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


@shared_task(bind=True)
def set_failed_charge():
    charges = PhoneCharge.objects.filter(
        Transaction__isnull=True, date_updated__gte=timedelta(days=1)
    )
    for charge in charges:
        try:
            transaction, created = Transaction.objects.get_or_create(
                tracking_code=charge.tracking_code
            )
            if created:
                continue
            transaction.wallet = charge.seller.user.wallet
            transaction.amount = charge.amount
            transaction.status = Transaction.StatusChoices.FAILURE
            transaction.action = Transaction.ActionChoices.DECREASE
            transaction.save()
        except OperationalError:
            continue
