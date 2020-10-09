from django.test import TestCase
from django.test import Client
from django.urls import reverse
from web_utils.http_status_codes import HTTP_200_OK
from snacks.models import SnackModel


class SnacksApiTests(TestCase):
    def test_list_snacks_endpoint(self):
        SnackModel(name='Snack A', price=1).save()
        SnackModel(name='Snack B', price=1.5).save()

        client = Client()
        response = client.get(path=reverse(viewname='snacks-api'))

        self.assertEqual(response.status_code, HTTP_200_OK)

        content = response.json()
        self.assertEqual(content['items'], [
            {'name': 'Snack A', 'price': 1},
            {'name': 'Snack B', 'price': 1.5}
        ])
