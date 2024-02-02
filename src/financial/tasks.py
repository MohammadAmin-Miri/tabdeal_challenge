from celery import shared_task
from django.db import transaction

from financial.models import Transaction, Wallet


@shared_task
@transaction.atomic
def create_transaction(transaction_id: int):
    transaction = Transaction.objects.get(id=transaction_id)
    wallet = transaction.wallet
    wallet.credit += transaction.amount
    wallet.save()
