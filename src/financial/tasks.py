from celery import shared_task
from django.db import transaction

from financial.models import Transaction, Wallet


@shared_task
@transaction.atomic
def create_transaction(tracking_code: str, amount: int, wallet_id: int):
    wallet = Wallet.objects.get(id=wallet_id)
    Transaction.objects.create(
        wallet=wallet,
        amount=amount,
        tracking_code=tracking_code,
        status=Transaction.StatusChoices.SUCCESS,
        action=Transaction.ActionChoices.INCREASE,
    )
    wallet.credit += amount
    wallet.save()
