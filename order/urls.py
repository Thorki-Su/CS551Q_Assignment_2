from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.all_orders, name='all_orders'),
]