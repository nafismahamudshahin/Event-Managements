from django.db import models
from django.contrib.auth.models import User , AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    profile_photo = models.ImageField(upload_to="profile_photos", blank=True , default="profile_photos/default_profile.jpg")
    bio = models.TextField(blank=True)
    phone_number = models.CharField(blank=True , max_length=13)

    def __str__(self):
        return self.username