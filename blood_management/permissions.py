from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Donor, BloodInventory, BloodRequest
from .serializer import DonorSerializer, BloodInventorySerializer, BloodRequestSerializer
from .permissions import IsAdminUser, IsRegularUser

# Donor Management View (Admin Only)
class DonorManagementView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only admin users can access this view

    def get(self, request):
        # Logic for retrieving donors (admin-only)
        return Response({"message": "Retrieve donor list (admin-only)"})

    def post(self, request):
        # Logic for adding a new donor (admin-only)
        return Response({"message": "Add a new donor (admin-only)"})

    def put(self, request, pk=None):
        # Logic for updating donor details (admin-only)
        return Response({"message": f"Update donor with id {pk} (admin-only)"})

    def delete(self, request, pk=None):
        # Logic for deleting a donor (admin-only)
        return Response({"message": f"Delete donor with id {pk} (admin-only)"})

# Blood Request View (Regular Users Only)
class BloodRequestView(APIView):
    permission_classes = [IsAuthenticated, IsRegularUser]  # Only regular users can access this view

    def post(self, request):
        # Logic for requesting blood (regular user)
        return Response({"message": "Request blood (regular user)"})
