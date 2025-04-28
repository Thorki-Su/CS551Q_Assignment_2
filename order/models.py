from django.db import models
from django.conf import settings

from user.models import User
from meteorite.models import Meteorite

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    meteorite = models.ForeignKey(Meteorite, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)