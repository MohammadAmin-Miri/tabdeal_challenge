from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from financial.models import Wallet
from .models import Seller


user_model = get_user_model()


@receiver(post_save, sender=user_model)
def create_seller_and_wallet(sender, instance, **kwargs):
    Wallet.objects.get_or_create(user=instance)
    Seller.objects.get_or_create(user=instance)
