from rest_framework import serializers
from .models import Donation
from django.contrib.auth import get_user_model
from .models import UserProfileModel
from .models import UserProfile
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User



class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer): 
     
     email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=UserProfile.objects.all())]
            )
     password = serializers.CharField(min_length=8, error_messages={'min_length': 'Password must have at least 8 characters.'})
     
     def create(self, validated_data):
        role = validated_data.pop('role')
        # Create user profile
        user_profile = UserProfile.objects.create(role=role, **validated_data)
          # Set the 'role' field after creating the user instance
        return user_profile
        # You can customize the UserProfile model fields as needed
     class Meta:
        model = UserProfile
        fields = ('username', 'email', 'role', 'password')
 # Add other fields as needed