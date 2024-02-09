from locust import HttpUser, task


class TestPhoneCharge(HttpUser):

    def on_start(self):
        res = self.client.post(
            "/api/auth/token/", json={"username": "admin", "password": "admin"}
        )
        self.token = res.json().get("access")
        self.client.post(
            "/api/financial/increase/",
            json={"amount": 100000},
            headers={"authorization": "Bearer " + self.token},
        )

    @task
    def test_phone_charge(self):
        self.client.post(
            "/api/users/charge/",
            json={"phone": "+989011111111", "amount": "10"},
            headers={"authorization": "Bearer " + self.token},
        )
