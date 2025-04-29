from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from user.models import User
from user.forms import UserRegistrationForm, UserLoginForm
from meteorite.models import Meteorite

class UserModuleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('user:register')
        self.login_url = reverse('user:login')
        self.logout_url = reverse('user:logout')
        self.profile_url = reverse('user:profile')
        for i in range(10):
            Meteorite.objects.create(
                name=f'Meteorite {i}', id=i+1, nametype='Type', recclass='Class', mass=100.0,
                fall='Fell', year=2020, latitude=0.0, longitude=0.0, price=100.00
            )

    def test_register_user_success(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'usertype': 'normal',
            'password1': 'P@ssw0rd123',
            'password2': 'P@ssw0rd123'
        }
        response = self.client.post(self.register_url, data)
        if response.status_code != 302:
            print(response.content.decode())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('meteorite:homepage'))
        user = User.objects.get(username='testuser')
        print(f"User usertype: {user.usertype}")
        self.assertEqual(user.usertype, 'normal')
        self.assertTrue(user.reg_time <= timezone.now())
        self.assertTrue(self.client.session.get('_auth_user_id'))

    def test_register_user_invalid_form(self):
        data = {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'different',
            'email': 'test@example.com',
            'usertype': 'normal'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.assertTemplateUsed(response, 'user/register.html')

    def test_login_user_success(self):
        User.objects.create_user(username='testuser', password='password123', usertype='normal')
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('meteorite:homepage'))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_user_invalid_credentials(self):
        User.objects.create_user(username='testuser', password='password123')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)
        self.assertTemplateUsed(response, 'user/login.html')

    def test_logout_user(self):
        User.objects.create_user(username='testuser', password='password123', usertype='normal')
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('meteorite:homepage'))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_profile_authenticated(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            usertype='normal'
        )
        login_success = self.client.login(username='testuser', password='password123')
        print(f"Login successful: {login_success}")
        response = self.client.get(self.profile_url)
        if response.status_code != 200:
            print(f"Redirect location: {response['Location']}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')

    def test_profile_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('user:login')}?next={self.profile_url}")