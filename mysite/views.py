from django.shortcuts import render
from user.models import User
from order.models import Order
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    users = User.objects.all()
    orders = Order.objects.all()

    return render(request, 'order/admin_dashboard.html', {
        'users': users,
        'orders': orders,
    })
