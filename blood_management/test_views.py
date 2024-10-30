from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Donor, BloodInventory, BloodRequest

class AdminEndpointsTests(APITestCase):
    def setUp(self):
        # Create an admin user and a regular user
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', is_staff=True)
        self.regular_user = User.objects.create_user(username='regularuser', password='regularpass', is_staff=False)

        # Set up clients for each user
        self.admin_client = APIClient()
        self.regular_client = APIClient()

        # Obtain JWT tokens for authentication
        admin_token = self.admin_client.post(reverse('token_obtain_pair'), {'username': 'admin', 'password': 'adminpass'}).data['access']
        regular_token = self.regular_client.post(reverse('token_obtain_pair'), {'username': 'regularuser', 'password': 'regularpass'}).data['access']

        # Set the Authorization header with the access token for both clients
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
        self.regular_client.credentials(HTTP_AUTHORIZATION=f'Bearer {regular_token}')

        # URL endpoints
        self.donors_url = reverse('donor_list_create')
        self.inventory_url = reverse('inventory_list_create')

    def test_admin_can_access_donors(self):
        response = self.admin_client.get(self.donors_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_cannot_access_donors(self):
        response = self.regular_client.get(self.donors_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_add_donor(self):
        data = {
            "name": "Jane Doe",
            "blood_type": "A+",
            "contact_info": "555-1234"
        }
        response = self.admin_client.post(self.donors_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_regular_user_cannot_add_donor(self):
        data = {
            "name": "John Doe",
            "blood_type": "B+",
            "contact_info": "555-5678"
        }
        response = self.regular_client.post(self.donors_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RegularUserEndpointsTests(APITestCase):
    def setUp(self):
        # Create a regular user and an admin user
        self.regular_user = User.objects.create_user(username='regularuser', password='regularpass', is_staff=False)
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', is_staff=True)

        # Set up clients
        self.regular_client = APIClient()
        self.admin_client = APIClient()

        # Obtain JWT tokens for authentication
        regular_token = self.regular_client.post(reverse('token_obtain_pair'), {'username': 'regularuser', 'password': 'regularpass'}).data['access']
        admin_token = self.admin_client.post(reverse('token_obtain_pair'), {'username': 'admin', 'password': 'adminpass'}).data['access']

        # Set the Authorization header with the access token
        self.regular_client.credentials(HTTP_AUTHORIZATION=f'Bearer {regular_token}')
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        # URL endpoint for creating blood requests
        self.requests_url = reverse('request_list_create')

    def test_regular_user_can_create_blood_request(self):
        data = {
            "blood_type": "A+",
            "units_requested": 2
        }
        response = self.regular_client.post(self.requests_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_cannot_create_blood_request_as_regular_user(self):
        data = {
            "blood_type": "O+",
            "units_requested": 3
        }
        response = self.admin_client.post(self.requests_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
