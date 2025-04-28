from django.shortcuts import render

# Create your views here.
def all_orders(request):
    return render(request,'order/order_main.html')