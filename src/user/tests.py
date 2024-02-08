from random import choice, randint
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from django.db.models import Sum
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from financial.models import Transaction


user_model = get_user_model()


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class ChargeFlowAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.first_user = user_model.objects.create(username="first_test_user")
        self.second_user = user_model.objects.create(username="second_test_user")

    def set_random_user_credentials(self):
        pks = user_model.objects.values_list("pk", flat=True)
        random_pk = choice(pks)
        random_user = user_model.objects.get(pk=random_pk)
        token = str(RefreshToken.for_user(random_user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    def test_charge_flow(self):

        for _ in range(10):
            self.set_random_user_credentials()
            res = self.client.post(
                reverse("increase-wallet-credit"),
                {"amount": randint(10000, 15000)},
            )
            self.assertEqual(res.status_code, 201)

        self.first_user.refresh_from_db()
        self.second_user.refresh_from_db()
        first_user_credit = self.first_user.wallet.credit
        second_user_credit = self.second_user.wallet.credit

        for _ in range(1000):
            self.set_random_user_credentials()
            res = self.client.post(
                reverse("charge-phone"),
                {"amount": randint(1, 100), "phone": "+989022222222"},
            )
            self.assertEqual(res.status_code, 201)

        self.first_user.refresh_from_db()
        self.second_user.refresh_from_db()
        first_user_current_credit = self.first_user.wallet.credit
        second_user_current_credit = self.second_user.wallet.credit

        first_user_decrease = (
            Transaction.objects.filter(
                wallet__user=self.first_user,
                status=Transaction.StatusChoices.SUCCESS,
                action=Transaction.ActionChoices.DECREASE,
            )
            .aggregate(decrease_amount=Sum("amount"))
            .get("decrease_amount")
        )
        second_user_decrease = (
            Transaction.objects.filter(
                wallet__user=self.second_user,
                status=Transaction.StatusChoices.SUCCESS,
                action=Transaction.ActionChoices.DECREASE,
            )
            .aggregate(decrease_amount=Sum("amount"))
            .get("decrease_amount")
        )

        self.assertEqual(
            first_user_credit, first_user_current_credit + first_user_decrease
        )
        self.assertEqual(
            second_user_credit, second_user_current_credit + second_user_decrease
        )
