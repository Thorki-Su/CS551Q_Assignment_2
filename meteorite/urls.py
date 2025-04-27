from django.urls import path

app_name = 'meteorite'

urlpatterns = [
    path('', views.homepage, name='homepage'),
]