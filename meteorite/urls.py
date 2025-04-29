from django.urls import path
from . import views

app_name = 'meteorite'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('list/', views.meteorite_list, name='meteorite_list'),
    path('detail/<int:meteorite_id>/', views.meteorite_detail, name='meteorite_detail'),
    path('set_marked/<int:meteorite_id>/', views.set_marked, name='set_marked'),
    path('compare_with_marked/<int:meteorite_id>/', views.compare_with_marked, name='compare_with_marked'),
    path('compare/<int:id1>/<int:id2>/', views.compare, name='compare'),
    path('clear_marked/', views.clear_marked, name='clear_marked'),
]