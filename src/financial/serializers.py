import uuid
from rest_framework import serializers

from financial.models import Transaction
from financial.tasks import create_transaction


class IncreaseCreditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ("tracking_code", "amount")
        read_only_fields = ("tracking_code",)
        extra_kwargs = {"amount": {"write_only": True}}

    def create(self, validated_data):
        transaction = super().create(validated_data)
        create_transaction.delay(transaction.id)
        return transaction
