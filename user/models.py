from django.db import models
from django.conf import settings

# Create your models here.
class User(models.Model):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('normal', 'Normal'),
    ]
    username = models.CharField(max_length=100, unique=True)
    usertype = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    email = models.EmailField()
    reg_time = models.DateTimeField(auto_now_add=True)