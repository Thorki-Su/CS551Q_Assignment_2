from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from user.models import User
from meteorite.models import Meteorite
from order.models import Cart, CartItem, Order, OrderItem
from decimal import Decimal

class OrderModuleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123', usertype='normal')
        self.meteorite = Meteorite.objects.create(
            name='Test Meteorite', id=1, nametype='Type', recclass='Class', mass=100.0,
            fall='Fall', year=2020, latitude=0.0, longitude=0.0, price=100.00
        )
        self.client.login(username='testuser', password='password123')
        self.cart = Cart.objects.create(user=self.user)
        self.add_to_cart_url = reverse('order:add_to_cart', args=[self.meteorite.id])
        self.view_cart_url = reverse('order:view_cart')
        self.checkout_url = reverse('order:checkout')
        self.my_orders_url = reverse('order:my_orders')
        self.buy_now_url = reverse('order:buy_now', args=[self.meteorite.id])

    def test_add_to_cart(self):
        """测试添加商品到购物车"""
        response = self.client.post(self.add_to_cart_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.view_cart_url)
        cart_item = CartItem.objects.get(cart=self.cart, meteorite=self.meteorite)
        self.assertEqual(cart_item.price, self.meteorite.price)

    def test_add_to_cart_duplicate(self):
        """测试重复添加商品到购物车"""
        CartItem.objects.create(cart=self.cart, meteorite=self.meteorite, price=self.meteorite.price)
        response = self.client.post(self.add_to_cart_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.cart.items.count(), 1)  # 不应重复添加

    def test_view_cart(self):
        """测试查看购物车内容"""
        CartItem.objects.create(cart=self.cart, meteorite=self.meteorite, price=self.meteorite.price)
        response = self.client.get(self.view_cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/cart.html')
        self.assertContains(response, 'Test Meteorite')
        self.assertContains(response, '100.00')  # 检查总价

    def test_checkout_success(self):
        """测试结账成功"""
        CartItem.objects.create(cart=self.cart, meteorite=self.meteorite, price=self.meteorite.price)
        response = self.client.post(self.checkout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.view_cart_url)
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.price, self.meteorite.price)
        order_item = OrderItem.objects.get(order=order, meteorite=self.meteorite)
        self.assertEqual(order_item.price, self.meteorite.price)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), f"Order placed successfully! Order ID: {order.id}")

    def test_checkout_empty_cart(self):
        """测试空购物车结账"""
        response = self.client.post(self.checkout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.view_cart_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Your cart is empty.")
        self.assertFalse(Order.objects.filter(user=self.user).exists())

    def test_buy_now_success(self):
        """测试立即购买"""
        response = self.client.post(self.buy_now_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.my_orders_url)
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.price, Decimal('100.00'))
        order_item = OrderItem.objects.get(order=order, meteorite=self.meteorite)
        self.assertEqual(order_item.price, Decimal('100.00'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), f"You have successfully purchased {self.meteorite.name}.")

    def test_my_orders(self):
        """测试查看我的订单"""
        Order.objects.create(user=self.user, price=100.00)
        response = self.client.get(self.my_orders_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/my_orders.html')
        self.assertContains(response, '100.00')