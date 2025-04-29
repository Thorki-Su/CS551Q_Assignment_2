from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:meteorite_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('buy-now/<int:meteorite_id>/', views.buy_now, name='buy_now'),
]