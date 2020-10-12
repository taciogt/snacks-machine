from django.test import Client
from django.test import TestCase
from django.urls import reverse

from core.snacks.entities import Snack
from snacks.repositories import DatabaseRepository
from web_utils.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


class SnacksApiTests(TestCase):
    def setUp(self) -> None:
        DatabaseRepository.clear_snacks()
        self.snack_a = DatabaseRepository.create_snack(Snack(name='Snack A', price=1))
        DatabaseRepository.create_snack(Snack(name='Snack B', price=1.5, available_quantity=2))

        self.client = Client()

    def test_list_snacks(self):
        response = self.client.get(path=reverse(viewname='snacks-api'))

        self.assertEqual(response.status_code, HTTP_200_OK)

        content = response.json()
        self.assertEqual(content['items'], [
            {'name': 'Snack A', 'price': 1, 'available_quantity': 0},
            {'name': 'Snack B', 'price': 1.5, 'available_quantity': 2}
        ])

    def test_recharge_snacks(self):
        data = {
            'name': self.snack_a.name,
            'quantity': 3
        }
        response = self.client.post(path=reverse(viewname='snacks-api'), data=data)

        self.assertEqual(response.status_code, HTTP_200_OK)
        content = response.json()
        self.assertEqual(content['snack'],
                         {'name': 'Snack A', 'price': 1, 'available_quantity': 3},
                         )

        snacks = DatabaseRepository.list_snacks()
        self.assertEqual(snacks[0],
                         Snack(name='Snack A', price=1.0, available_quantity=3)
                         )

    def test_recharge_snacks_with_invalid_quantity(self):
        data = {
            'name': self.snack_a.name,
            'quantity': -1
        }
        response = self.client.post(path=reverse(viewname='snacks-api'), data=data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        content = response.content.decode()
        self.assertEqual(content, 'NegativeSnackQuantityError')

        snacks = DatabaseRepository.list_snacks()
        self.assertEqual(snacks[0],
                         Snack(name='Snack A', price=1.0, available_quantity=0)
                         )

    def test_recharge_snacks_with_invalid_name(self):
        data = {
            'name': 'invalid-name',
            'quantity': 1
        }
        response = self.client.post(path=reverse(viewname='snacks-api'), data=data)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        content = response.content.decode()
        self.assertEqual(content, 'Snack "invalid-name" not found.')
