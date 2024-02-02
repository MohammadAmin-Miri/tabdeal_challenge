import uuid
from rest_framework import serializers

from user.tasks import create_phone_charge


class PhoneChargeSerializer(serializers.Serializer):
    tracking_code = serializers.UUIDField(read_only=True)
    phone = serializers.RegexField(r"^(\+98|0)?9\d{9}$", max_length=15, write_only=True)
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        fields = ("tracking_code", "phone", "amount")

    def create(self, validated_data):
        tracking_code = uuid.uuid4()
        create_phone_charge.delay(
            str(tracking_code),
            validated_data.get("amount"),
            validated_data.get("phone"),
            validated_data.get("seller"),
        )
        return {"tracking_code": tracking_code}
