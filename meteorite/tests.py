from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from user.models import User
from meteorite.models import Meteorite

class MeteoriteModuleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123', usertype='normal')
        self.client.login(username='testuser', password='password123')
        self.meteorites = []
        # 创建第一个陨石
        self.meteorite1 = Meteorite.objects.create(
            name='Test Meteorite', id=1, nametype='Type', recclass='Class', mass=100.0,
            fall='Fell', year=2020, latitude=0.0, longitude=0.0, price=100.00
        )
        self.meteorites.append(self.meteorite1)
        # 创建第二个陨石
        self.meteorite2 = Meteorite.objects.create(
            name='Another Meteorite', id=2, nametype='Type', recclass='Class', mass=50.0,
            fall='Found', year=1990, latitude=1.0, longitude=1.0, price=50.00
        )
        self.meteorites.append(self.meteorite2)
        # 创建剩余 8 个陨石，调整名称以匹配 'Meteorite 0' 等
        for i in range(3, 11):
            meteorite = Meteorite.objects.create(
                name=f'Meteorite {i-3}', id=i, nametype='Type', recclass='Class', mass=100.0,
                fall='Fell', year=2020, latitude=0.0, longitude=0.0, price=100.00
            )
            self.meteorites.append(meteorite)
        self.homepage_url = reverse('meteorite:homepage')
        self.list_url = reverse('meteorite:meteorite_list')
        self.detail_url = reverse('meteorite:meteorite_detail', args=[self.meteorite1.id])
        self.set_marked_url = reverse('meteorite:set_marked', args=[self.meteorite1.id])
        self.compare_with_marked_url = reverse('meteorite:compare_with_marked', args=[self.meteorite2.id])
        self.compare_url = reverse('meteorite:compare', args=[self.meteorite1.id, self.meteorite2.id])

    def test_homepage(self):
        """测试陨石模块主页"""
        response = self.client.get(self.homepage_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meteorite/homepage.html')
        self.assertContains(response, 'Meteorite 0')

    def test_meteorite_list(self):
        """测试陨石列表页面"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meteorite/list.html')
        self.assertContains(response, 'Test Meteorite')
        self.assertContains(response, 'Another Meteorite')

    def test_meteorite_list_search(self):
        """测试陨石列表搜索功能"""
        response = self.client.get(self.list_url, {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Meteorite')
        self.assertNotContains(response, 'Another Meteorite')
        response = self.client.get(self.list_url, {'search': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Meteorite')

    def test_meteorite_list_sort(self):
        """测试陨石列表排序功能"""
        response = self.client.get(self.list_url, {'sort': 'mass_asc'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Another Meteorite')  # mass=50 在前
        self.assertContains(response, 'Test Meteorite')  # mass=100 在后

    def test_meteorite_list_filter(self):
        """测试陨石列表过滤功能"""
        response = self.client.get(self.list_url, {'fall': 'Fell'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Meteorite')
        self.assertNotContains(response, 'Another Meteorite')
        response = self.client.get(self.list_url, {'year': 'before_2000'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Another Meteorite')
        self.assertNotContains(response, 'Test Meteorite')

    def test_meteorite_detail(self):
        """测试陨石详情页面"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meteorite/detail.html')
        self.assertContains(response, 'Test Meteorite')
        self.assertContains(response, 'Class')  # 检查 similar_meteorites

    def test_set_marked(self):
        """测试标记陨石"""
        response = self.client.post(self.set_marked_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.detail_url)
        self.assertEqual(self.client.session['marked_id'], self.meteorite1.id)

    def test_compare_with_marked_no_mark(self):
        """测试未标记时的比较"""
        response = self.client.get(self.compare_with_marked_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('meteorite:meteorite_detail', args=[self.meteorite2.id]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "No meteorite has been marked for comparison.")

    def test_compare_with_marked_same_meteorite(self):
        """测试比较相同陨石"""
        # 模拟调用 set_marked 视图
        response = self.client.post(reverse('meteorite:set_marked', args=[self.meteorite1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get('marked_id'), self.meteorite1.id)
        # 测试 compare_with_marked
        response = self.client.get(reverse('meteorite:compare_with_marked', args=[self.meteorite1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('meteorite:meteorite_detail', args=[self.meteorite1.id]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "You're comparing the same meteorite.")

    def test_compare(self):
        """测试陨石比较页面"""
        response = self.client.get(self.compare_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meteorite/compare.html')
        self.assertContains(response, 'Test Meteorite')
        self.assertContains(response, 'Another Meteorite')