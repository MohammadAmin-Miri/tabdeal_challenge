from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user.serializers import PhoneChargeSerializer


class ChargeAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhoneChargeSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.seller.id)
