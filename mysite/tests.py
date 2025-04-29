from django.test import TestCase, Client
from django.urls import reverse
from user.models import User
from order.models import Order

class MySiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_dashboard_url = reverse('admin_dashboard')
        self.admin = User.objects.create_superuser(username='admin', password='admin123', email='admin@example.com')
        self.normal_user = User.objects.create_user(username='normal', password='normal123', usertype='normal')

    def test_admin_dashboard_superuser(self):
        """测试超级用户访问仪表盘"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(self.admin_dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/admin_dashboard.html')
        self.assertContains(response, 'admin')  # 检查用户数据是否渲染

    def test_admin_dashboard_normal_user(self):
        """测试普通用户无权访问仪表盘"""
        self.client.login(username='normal', password='normal123')
        response = self.client.get(self.admin_dashboard_url)
        self.assertEqual(response.status_code, 302)  # 重定向到登录页或403
        self.assertNotEqual(response.status_code, 200)

    def test_admin_dashboard_unauthenticated(self):
        """测试未登录用户访问仪表盘"""
        response = self.client.get(self.admin_dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('user:login')}?next={self.admin_dashboard_url}")