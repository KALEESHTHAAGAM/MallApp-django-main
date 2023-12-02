from sys import setprofile
from typing import Self
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.contrib.auth import get_user_model
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry, ADDITION




# Create your models here.
class donar_data(models.Model):

    name = models.CharField(max_length=100)
    nameOnParcel = models.CharField(max_length=100)
    mobileNumber = models.CharField(max_length=15)
    selectedCategory = models.CharField(max_length=100)
  
    count = models.IntegerField()
    enteredAmount = models.DecimalField(max_digits=10, decimal_places=2)
   
    # Add other fields as needed

    def __str__(self):
        return f"name: {self.name}, Name on Parcel: {self.nameOnParcel}, Mobile Number: {self.mobileNumber}, Category: {self.selectedCategory},Count: {self.count},enteredAmount: {self.enteredAmount}"
    
    
class Donation(models.Model):
   
    enteredAmount = models.DecimalField(max_digits=10, decimal_places=2)
    
class CollectionData(models.Model):
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()
    
    def __str__(self):
        return f'enteredAmount: {self.Amount}, Timestamp: {self.timestamp}'
    



class UserProfileManager(BaseUserManager):
    def create_user(self,  email, password, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        UserProfile = self.model(email=self.normalize_email(email),password=password **extra_fields)
        UserProfile.set_password(password)
        UserProfile.save()
        return UserProfile

class UserProfile(AbstractBaseUser, PermissionsMixin):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150,unique=True)
    role =models.CharField(max_length=150)
    password = models.CharField(max_length=150)  
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    


class UserProfileModel(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    coins = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Any additional logic you want to include before saving
        super(UserProfileModel, self).save(*args, **kwargs)