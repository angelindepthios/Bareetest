from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    SKIN_TYPE_CHOICES = [
        ('combination', 'Combination'),
        ('normal', 'Normal'),
        ('oily', 'Oily'),
        ('dry', 'Dry'),
        ('sensitive', 'Sensitive'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES, blank=True, null=True
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_photo = models.URLField(max_length=200, blank=True, null=True)
    skintype = models.CharField(
        max_length=15, choices=SKIN_TYPE_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return self.username
