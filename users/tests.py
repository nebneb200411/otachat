from django.test import Client, TestCase
from .models import User


class TestCase(TestCase):
    """
    """

    def setUp(self):
        """
        """
        self.user = User.objects.create_user(
            'Yuya', 'watanabenabeyuya@yahoo.co.jp', 'password')

        self.client = Client()

        self.client.login(username='Yuya', password='password')
