from celery import shared_task
from django.db import OperationalError, transaction

from financial.models import Transaction, Wallet


@shared_task
@transaction.atomic
def create_transaction(transaction_id: int):
    transaction = Transaction.objects.select_for_update().get(id=transaction_id)
    transaction.status = Transaction.StatusChoices.SUCCESS
    transaction.save()
    wallet = Wallet.objects.select_for_update().get(id=transaction.wallet.id)
    wallet.credit += transaction.amount
    wallet.save()
