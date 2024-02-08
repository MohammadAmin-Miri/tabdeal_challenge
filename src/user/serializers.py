import uuid
from rest_framework import serializers
from user.models import PhoneCharge

from user.tasks import create_phone_charge


class PhoneChargeSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(write_only=True, min_value=0)
    tracking_code = serializers.CharField(read_only=True)

    class Meta:
        model = PhoneCharge
        fields = ("tracking_code", "phone", "amount")
        read_only_fields = ("tracking_code",)
        extra_kwargs = {
            "phone": {"write_only": True},
        }

    def create(self, validated_data):
        amount = validated_data.pop("amount")
        phone_charge = super().create(validated_data)
        tracking_code = str(uuid.uuid4())
        create_phone_charge.delay(phone_charge.id, amount, tracking_code)
        return {"tracking_code": tracking_code}
