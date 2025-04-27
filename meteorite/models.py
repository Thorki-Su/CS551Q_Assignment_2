from django.db import models
from django.conf import settings

# Create your models here.
class Meteorite(models.Model):
    name = models.CharField(max_length=100, unique=True)
    id = models.IntegerField(primary_key=True)
    nametype = models.CharField(max_length=20)
    recclass = models.CharField(max_length=50)
    mass = models.FloatField()
    fall = models.CharField(max_length=20)
    year = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class User(models.Model):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('normal', 'Normal'),
    ]
    username = models.CharField(max_length=100, unique=True)
    usertype = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    email = models.EmailField()
    reg_time = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    meteorite = models.ForeignKey(Meteorite, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)