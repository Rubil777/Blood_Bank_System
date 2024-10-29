from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Donor, BloodInventory, BloodRequest
from blood_management.serializer import DonorSerializer, BloodInventorySerializer, BloodRequestSerializer
from .permissions import IsAdminUser, IsRegularUser

# Donor Management (Admin Only)
class DonorListCreateView(generics.ListCreateAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


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
        # Custom logic, if needed, can be added here before saving
        serializer.save()


class BloodInventoryDetailView(generics.RetrieveUpdateAPIView):
    queryset = BloodInventory.objects.all()
    serializer_class = BloodInventorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


# Blood Requests (Regular Users Only)
class BloodRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAuthenticated, IsRegularUser]

    def get_queryset(self):
        # Filter requests to show only those made by the current user
        return BloodRequest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user making the request
        serializer.save(user=self.request.user)


class BloodRequestAdminListView(generics.ListAPIView):
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
