from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Donor, BloodInventory, BloodRequest
from django.test import TestCase

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_credentials = {"username": "admin", "password": "adminpassword"}
        User.objects.create_superuser(**self.admin_credentials)
    
    def test_login(self):
        response = self.client.post("/api/token/", self.admin_credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh(self):
        login_response = self.client.post("/api/token/", self.admin_credentials)
        refresh_token = login_response.data["refresh"]
        response = self.client.post("/api/token/refresh/", {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)


class DonorManagementTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass")
        self.client.login(username="admin", password="adminpass")

    def test_create_donor(self):
        response = self.client.post("/api/donors/", {
            "name": "Jane Doe",
            "blood_type": "B+",
            "contact_info": "9876543210",
            "last_donation_date": "2023-08-01"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Jane Doe")

    def test_donor_list(self):
        response = self.client.get("/api/donors/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BloodInventoryTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass")
        self.client.login(username="admin", password="adminpass")
        self.inventory = BloodInventory.objects.create(blood_type="A+", units_available=10)

    def test_update_inventory(self):
        response = self.client.put(f"/api/inventory/{self.inventory.id}/", {"units_available": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.units_available, 5)


class BloodRequestTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass")
        self.regular_user = User.objects.create_user(username="user", password="userpass")
        self.client.login(username="user", password="userpass")

    def test_create_blood_request(self):
        response = self.client.post("/api/requests/", {
            "blood_type": "A+",
            "units_requested": 2
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "Pending")

    def test_admin_fulfill_request(self):
        # Create a request as regular user
        request = BloodRequest.objects.create(
            user=self.regular_user, blood_type="A+", units_requested=2, status="Pending"
        )
        
        # Admin fulfills the request
        self.client.logout()
        self.client.login(username="admin", password="adminpass")
        response = self.client.put(f"/api/admin/requests/{request.id}/", {"status": "Fulfilled"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request.refresh_from_db()
        self.assertEqual(request.status, "Fulfilled")
