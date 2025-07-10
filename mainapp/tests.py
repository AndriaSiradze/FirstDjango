from django.test import TestCase

# Create your tests here.

from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

class SmokeTestPages(TestCase):

    def test_main_page_open(self):
        path = reverse('mainapp:main_page')
        result = self.client.get(path)

        self.assertEqual(HTTPStatus.OK, result.status_code)
