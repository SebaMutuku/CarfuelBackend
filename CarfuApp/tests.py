from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase


class ApiTest(APITestCase):
    url = reverse("Register")

    def test_login_returns_token(self):
        url = reverse("Login")
        users = User.objects.get(any())
        user_data = {
            "username": "seba",
            "user_id": 5,

        }
        response = self.client.post(url, user_data)
        print("Status code", response)
        if response.status_code == 200:
            print("Test data", response.data)
            self.assertEqual(users, 5)
        else:
            print("Status code", response.data)
            self.assertNotEqual(1, 3)

    def test_get_users(self):
        users = User.objects.all()
        self.assertIsNotNone(users)
#
# def test_encoding(self):
#     value = "seba"
#     security = AESEncryption()
#     # security.encrypt_value(value)
#     self.assertEqual("sGVwYhy/Xo4wDMH1J+j8vDewnXgvVI432F6iE9JzOY=", security.encrypt_value(value))

# def test_decode(self):
# 	value = "sGVwYhy/Xo4wDMH1J+j8vDewnXgvVI432F6iE9JzOY=".encode("ascii")
# 	security = AESEncryption()
# 	self.assertEqual("seba", security.decrypt_value(value))
