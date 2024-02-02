import uuid
from rest_framework import serializers
from user.models import PhoneCharge

from user.tasks import create_phone_charge


class PhoneChargeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhoneCharge
        fields = ("tracking_code", "phone", "amount")
        read_only_fields = ("tracking_code",)
        extra_kwargs = {
            "phone": {"write_only": True},
            "amount": {"write_only": True},
        }

    def create(self, validated_data):
        phone_charge = super().create(validated_data)
        create_phone_charge.delay(phone_charge.id)
        return phone_charge
