from django.shortcuts import render
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Donor, BloodInventory, BloodRequest
from .serializer import DonorSerializer, BloodInventorySerializer, BloodRequestSerializer, UserRegistrationSerializer
from .permissions import IsAdminUser, IsRegularUser

# Donor Management (Admin Only)
class DonorListCreateView(generics.ListCreateAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['blood_type', 'last_donation_date']  # Filter by blood type and last donation date

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
    filter_backends = [filters.SearchFilter]
    search_fields = ['blood_type', 'status']  # Filter by blood type and status


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    