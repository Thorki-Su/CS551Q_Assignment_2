from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, CartItem, Order, OrderItem
from meteorite.models import Meteorite
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from decimal import Decimal

# Create your views here.
@login_required
def add_to_cart(request, meteorite_id):
    meteorite = get_object_or_404(Meteorite, pk=meteorite_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if not cart.items.filter(meteorite=meteorite).exists():
        CartItem.objects.create(cart=cart, meteorite=meteorite, price=meteorite.price)

    return redirect('order:view_cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('meteorite')
    total_price = sum(item.price for item in items)
    return render(request, 'order/cart.html', {
        'items': items,
        'total_price': total_price,
    })

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('order:view_cart')

@login_required
@transaction.atomic
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()

    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect('order:view_cart')

    # Create an order
    total_price = sum(item.price for item in items)
    order = Order.objects.create(user=request.user, price=total_price)

    for item in items:
        OrderItem.objects.create(
            order=order,
            meteorite=item.meteorite,
            price=item.price,
        )

    # Empty Cart
    items.delete()

    messages.success(request, f"Order placed successfully! Order ID: {order.id}")
    return redirect('order:view_cart')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'order/my_orders.html', {'orders': orders})

@login_required
@transaction.atomic
def buy_now(request, meteorite_id):
    meteorite = get_object_or_404(Meteorite, id=meteorite_id)
    
    # Create an order
    order = Order.objects.create(
        user=request.user,
        price=Decimal(meteorite.price)
    )
    
    OrderItem.objects.create(
        order=order,
        meteorite=meteorite,
        price=Decimal(meteorite.price)
    )

    messages.success(request, f'You have successfully purchased {meteorite.name}.')
    return redirect('order:my_orders')