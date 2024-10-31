from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Donor, BloodInventory, BloodRequest

# Authentication Tests
class AuthenticationTest(APITestCase):
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

# Donor Management Tests (Admin Only)
class DonorManagementTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass")
        
        # Authenticate as admin with JWT
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

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

# Blood Inventory Management Tests (Admin Only)
class BloodInventoryTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass")
        
        # Authenticate as admin with JWT
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Set up inventory item
        self.inventory = BloodInventory.objects.create(blood_type="A+", units_available=10)

    def test_update_inventory(self):
        response = self.client.put(f"/api/inventory/{self.inventory.id}/", {"blood_type": "A+", "units_available": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.units_available, 5)

# Blood Request Management Tests
class BloodRequestTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass")
        self.regular_user = User.objects.create_user(username="user", password="userpass")
        
        # Authenticate as regular user
        refresh = RefreshToken.for_user(self.regular_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Create an inventory item for testing
        self.inventory = BloodInventory.objects.create(blood_type="A+", units_available=10)

    def test_create_blood_request(self):
        # Test creating a blood request
        response = self.client.post("/api/requests/", {
            "blood_type": "A+",
            "units_requested": 2
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "Pending")

    def test_admin_fulfill_request(self):
        # Create a blood request as a regular user
        request = BloodRequest.objects.create(
            user=self.regular_user,
            blood_type="A+",
            units_requested=2,
            status="Pending"
        )
        
        print("Created BloodRequest ID:", request.id)  # Debugging output

        # Re-authenticate as admin for fulfilling the request
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        url = f"/api/admin/requests/{request.id}/"
        print("PUT Request URL:", url)

        # Make the PUT request as admin to fulfill the blood request
        response = self.client.put(url, {"status": "Fulfilled"})
        print("Response status code:", response.status_code)  # Debugging output
        print("Response data:", response.data)  # Check for any error details in response

        # Assert that the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Reload the blood request instance from the database
        request.refresh_from_db()
        self.assertEqual(request.status, "Fulfilled")  # Verify that the status has been updated