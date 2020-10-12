from django.test import Client
from django.test import TestCase
from django.urls import reverse

from core.snacks.entities import Snack
from core.currency.entities import Cash
from snacks.services import repository as snacks_repository
from currency.services import repository as cash_repository
from web_utils.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_402_PAYMENT_REQUIRED, \
    HTTP_404_NOT_FOUND


class SnacksEndpointTests(TestCase):
    path = reverse(viewname='snacks-endpoint')

    def setUp(self) -> None:
        snacks_repository.clear_snacks()
        self.snack_a = snacks_repository.create_snack(Snack(name='Snack A', price=1))
        snacks_repository.create_snack(Snack(name='Snack B', price=1.5, available_quantity=2))

        self.client = Client()

    def test_list_snacks(self):
        response = self.client.get(path=self.path)

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
        response = self.client.post(path=self.path, data=data)

        self.assertEqual(response.status_code, HTTP_200_OK)
        content = response.json()
        self.assertEqual(content['snack'],
                         {'name': 'Snack A', 'price': 1, 'available_quantity': 3},
                         )

        snacks = snacks_repository.list_snacks()
        self.assertEqual(snacks[0],
                         Snack(name='Snack A', price=1.0, available_quantity=3)
                         )

    def test_recharge_snacks_with_invalid_quantity(self):
        data = {
            'name': self.snack_a.name,
            'quantity': -1
        }
        response = self.client.post(path=self.path, data=data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        content = response.content.decode()
        self.assertEqual(content, 'NegativeSnackQuantityError')

        snacks = snacks_repository.list_snacks()
        self.assertEqual(snacks[0],
                         Snack(name='Snack A', price=1.0, available_quantity=0)
                         )

    def test_recharge_snacks_with_invalid_name(self):
        data = {
            'name': 'invalid-name',
            'quantity': 1
        }
        response = self.client.post(path=self.path, data=data)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        content = response.content.decode()
        self.assertEqual(content, 'Snack "invalid-name" not found.')


class BuySnacksEndpointTests(TestCase):
    def setUp(self) -> None:
        snacks_repository.clear_snacks()
        self.snack = snacks_repository.create_snack(Snack(name='Snack A', price=2))

        self.client = Client()

    def test_buy_snack(self):
        cash_repository.insert_wallet_cash(cash=Cash(2))
        data = {
            'name': self.snack.name,
        }
        response = self.client.post(path=reverse(viewname='buy_snacks-endpoint'), data=data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        content = response.json()
        self.assertEqual(content,
                         {'change': []})

    def test_buy_snack_with_insufficient_cash(self):
        cash_repository.insert_wallet_cash(cash=Cash(.5))
        data = {
            'name': self.snack.name,
        }
        response = self.client.post(path=reverse(viewname='buy_snacks-endpoint'), data=data)

        self.assertEqual(response.status_code, HTTP_402_PAYMENT_REQUIRED)

        content = response.content.decode()
        self.assertEqual(content, 'Insufficient cash. Provided: R$ 0.50. Required: R$ 2.00')
