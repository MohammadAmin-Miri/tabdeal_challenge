from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from financial.serializers import IncreaseCreditSerializer


class IncreaseWalletCreditAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IncreaseCreditSerializer

    def perform_create(self, serializer):
        serializer.save(wallet=self.request.user.wallet.id)
