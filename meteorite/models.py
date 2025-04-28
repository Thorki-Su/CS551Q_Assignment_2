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