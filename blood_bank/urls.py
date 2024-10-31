

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from blood_management.views import (
    DonorListCreateView, DonorDetailView,
    BloodInventoryListCreateView, BloodInventoryDetailView,
    BloodRequestAdminListView, BloodRequestListCreateView,
    UserRegistrationView,BloodRequestAdminDetailView
)

def home_view(request):
    return HttpResponse("Welcome to the Blood Bank API")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', UserRegistrationView.as_view(), name='register'),

    # Donor URLs (Admins)
    path('api/donors/', DonorListCreateView.as_view(), name='donor_list_create'),
    path('api/donors/<int:pk>/', DonorDetailView.as_view(), name='donor_detail'),

    # Blood Inventory URLs (Admins)
    path('api/inventory/', BloodInventoryListCreateView.as_view(), name='inventory_list_create'),
    path('api/inventory/<int:pk>/', BloodInventoryDetailView.as_view(), name='inventory_detail'),

    # Blood Request URLs (Regular Users and Admins)
    path('api/requests/', BloodRequestListCreateView.as_view(), name='request_list_create'),
    path('api/admin/requests/', BloodRequestAdminListView.as_view(), name='admin_request_list'),
    path('api/admin/requests/<int:pk>/', BloodRequestAdminDetailView.as_view(), name='admin_request_detail'),
]
