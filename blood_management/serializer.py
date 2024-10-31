from rest_framework import serializers
from .models import Donor, BloodInventory, BloodRequest
from django.contrib.auth.models import User
from rest_framework import serializers

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'


class BloodInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodInventory
        fields = '__all__'


class BloodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodRequest
        fields = '__all__'
        read_only_fields = ['status', 'request_date', 'user']  # These fields are read-only

    blood_type = serializers.CharField(required=True)  # Ensure required fields
    units_requested = serializers.IntegerField(required=True)


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}  # Ensure email is required
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
