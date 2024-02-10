from celery import shared_task
from django.db import OperationalError, transaction

from financial.models import Transaction, Wallet


@shared_task(
    bind=True,
    autoretry_for=(OperationalError,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 20},
)
@transaction.atomic
def create_transaction(transaction_id: int):
    transaction = Transaction.objects.select_for_update().get(id=transaction_id)
    transaction.status = Transaction.StatusChoices.SUCCESS
    transaction.save()
    wallet = transaction.wallet
    wallet.credit += transaction.amount
    wallet.save()
