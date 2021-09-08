from django.test import TestCase
from rest_framework.test import  APITestCase
from django.urls import reverse

from CarfuApp.models import Users


class ApiTest(APITestCase):
	url=reverse("Register")
	def test_all_users(self):
		url=reverse("Login")
		users=Users.objects.all()
		user_data={
			"username":"seba",
			"user_id":5,

		}
		response=self.client.post(url,user_data)
		print("Status code", response)
		if response.status_code==200:
			print("Test data",response.data)
			self.assertEqual(users,5)
		else:
			print("Status code",response.data)
			self.assertNotEqual(1,3)
	
	def test_get_users(self):
		users=Users.objects.all()
		response=self.client.get(self.url)
		if response.status_code==200:
			self.assertEqual(users,response.data)
		else:
			self.assertEqual(None,response.data)
	
