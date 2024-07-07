from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
import datetime

from accounts.models import Organization

User = get_user_model()


class TokenGenerationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )

    def test_token_contains_correct_user_details(self):
        token = AccessToken.for_user(self.user)
        self.assertEqual(token['user_id'], str(self.user.user_id))
        self.assertEqual(token['email'], self.user.email)

    def test_token_expiration(self):
        token = AccessToken.for_user(self.user)
        expiration_time = datetime.datetime.fromtimestamp(token['exp'])
        current_time = datetime.datetime.now()
        self.assertTrue(expiration_time > current_time)


class OrganizationAccessTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123')
        self.org1 = Organization.objects.create(name="Org1", owner=self.user1)
        self.org2 = Organization.objects.create(name="Org2", owner=self.user2)

    def test_user_cannot_access_other_organizations_data(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/organizations/{self.org2.id}/')
        self.assertEqual(response.status_code, 403)
