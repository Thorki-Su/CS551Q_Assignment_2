from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('normal', 'Normal'),
    ]
    usertype = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    reg_time = models.DateTimeField(auto_now_add=True)
