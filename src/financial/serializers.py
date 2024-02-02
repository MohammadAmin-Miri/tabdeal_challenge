import uuid
from rest_framework import serializers

from financial.models import Transaction
from financial.tasks import create_transaction


class IncreaseCreditSerializer(serializers.Serializer):
    tracking_code = serializers.UUIDField()
    amount = serializers.IntegerField(write_only=True)
    wallet = serializers.IntegerField(write_only=True)

    class Meta:
        fields = ("tracking_code", "amount", "wallet")
        read_only_fields = "tracking_code"

    def create(self, validated_data):
        tracking_code = uuid.uuid4()
        create_transaction.delay(
            tracking_code, validated_data.get("amount"), validated_data.get("wallet")
        )
        return {"tracking_code": tracking_code}
