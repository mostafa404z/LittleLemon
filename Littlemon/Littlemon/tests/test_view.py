from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User 
from rest_framework import status
from rest_framework.test import APIClient
from restaurant.models import Menu
from restaurant.serializers import MenuItemSerializer

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        
        Menu.objects.create(title="IceCream", price=80, inventory=True)
        Menu.objects.create(title="Pizza", price=120, inventory=False)
        Menu.objects.create(title="Burger", price=90, inventory=True)

    def test_getall(self):
        items = Menu.objects.all()
        serialized_data = MenuItemSerializer(items, many=True).data
        
        response = self.client.get(reverse('menu'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_data)