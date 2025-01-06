# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserViewsTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/register/' 
        self.login_url = '/api/login/' 
        
        self.valid_user_data = {
            'username': 'testuser',
            'password': 'securepassword123',
            'email': 'testuser@example.com'
        }
        
        self.valid_login_data = {
            'username': 'testuser',
            'password': 'securepassword123'
        }

    def test_register_user_success(self):
        """
        Test successful user registration.
        """
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)

    def test_register_user_invalid_data(self):
        """
        Test registration with missing or invalid data.
        """
        invalid_data = { 
            'username': 'testuser',
            'email': 'testuser@example.com'
        }
        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_login_success(self):
        """
        Test successful login with valid credentials.
        """
        self.client.post(self.register_url, self.valid_user_data, format='json')
        
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('role', response.data)
        
        user = User.objects.get(username=self.valid_user_data['username'])
        token = Token.objects.get(user=user)
        self.assertEqual(token.key, response.data['token'])

    def test_login_invalid_credentials(self):
        """
        Test login with invalid credentials.
        """
        # Attempt login with wrong password
        invalid_login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, invalid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_login_user_not_registered(self):
        """
        Test login attempt for a user who hasn't registered yet.
        """
        invalid_login_data = {
            'username': 'nonexistentuser',
            'password': 'somepassword'
        }
        response = self.client.post(self.login_url, invalid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_user_role_assigned_on_login(self):
        """
        Ensure that user roles are correctly assigned during login.
        """
        staff_user = User.objects.create_user(username='staffuser', password='staffpassword', email='staff@example.com')
        staff_user.is_staff = True
        staff_user.save()
        
        login_data = {
            'username': 'staffuser',
            'password': 'staffpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'staff')

        superuser = User.objects.create_user(username='superuser', password='superpassword', email='superuser@example.com')
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save()

        login_data = {
            'username': 'superuser',
            'password': 'superpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'superuser')

        regular_user = User.objects.create_user(username='regularuser', password='regularpassword', email='regular@example.com')

        login_data = {
            'username': 'regularuser',
            'password': 'regularpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'patient')

