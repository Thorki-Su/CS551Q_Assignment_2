from django.urls import path
from . import views

app_name = 'meteorite'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('list/', views.meteorite_list, name='meteorite_list'),
    path('detail/<int:meteorite_id>/', views.meteorite_detail, name='meteorite_detail'),
]