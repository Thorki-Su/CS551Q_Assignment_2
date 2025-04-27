from django.urls import path
from . import views

app_name = 'meteorite'

urlpatterns = [
    path('', views.homepage, name='homepage'),
]