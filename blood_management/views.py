from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import generics, status, filters
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Donor, BloodInventory, BloodRequest
from .serializer import DonorSerializer, BloodInventorySerializer, BloodRequestSerializer, UserRegistrationSerializer
from .permissions import IsAdminUser, IsRegularUser

# Function to check low inventory and send email notifications
def check_low_inventory():
    critical_level = 5  # Set threshold for low inventory
    low_inventory = BloodInventory.objects.filter(units_available__lt=critical_level)

    if low_inventory.exists():
        blood_types = ', '.join([inventory.blood_type for inventory in low_inventory])
        send_mail(
            'Critical Blood Inventory Alert',
            f'The following blood types are below critical levels: {blood_types}. Please replenish soon.',
            settings.DEFAULT_FROM_EMAIL,
            ['placeholder@example.com'],  # Placeholder email since local testing
        )

# Donor Management (Admin Only)
class DonorListCreateView(generics.ListCreateAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'blood_type', 'contact_info', 'last_donation_date']

class DonorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

# Blood Inventory Management (Admin Only)
class BloodInventoryListCreateView(generics.ListCreateAPIView):
    queryset = BloodInventory.objects.all()
    serializer_class = BloodInventorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()
        check_low_inventory()  # Check levels after creating a new inventory entry

class BloodInventoryDetailView(generics.RetrieveUpdateAPIView):
    queryset = BloodInventory.objects.all()
    serializer_class = BloodInventorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_update(self, serializer):
        serializer.save()
        check_low_inventory()  # Check levels after updating inventory

# Blood Requests (Regular Users Only)
class BloodRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAuthenticated, IsRegularUser]

    def get_queryset(self):
        return BloodRequest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BloodRequestAdminListView(generics.ListAPIView):
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['blood_type', 'status']

# User Registration View
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BloodRequestAdminDetailView(RetrieveUpdateAPIView):
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print("Accessed BloodRequest ID:", instance.id)  # Debugging output

        # Get the new status from the request data
        new_status = request.data.get("status")

        # Only proceed if changing status to "Fulfilled" and inventory allows it
        if new_status == "Fulfilled" and instance.status != "Fulfilled":
            inventory_item = get_object_or_404(BloodInventory, blood_type=instance.blood_type)
            if inventory_item.units_available < instance.units_requested:
                raise ValidationError("Not enough units available in inventory to fulfill this request.")

            inventory_item.units_available -= instance.units_requested
            inventory_item.save()
            check_low_inventory()

        return super().update(request, *args, **kwargs)
