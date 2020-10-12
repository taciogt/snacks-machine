from django.test import Client
from django.test import TestCase
from django.urls import reverse

from web_utils.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from currency.services import repository
from core.currency.entities import Cash


class InsertCashEndpointTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()

    def test_insert_cash(self):
        response = self.client.post(path=reverse(viewname='currency-api'), data={'cash_value': 2})

        self.assertEqual(response.status_code, HTTP_200_OK)
        content = response.json()
        self.assertEqual(content, {
            'cash_amount': [2],
            'total_value': 2
        })

        response = self.client.post(path=reverse(viewname='currency-api'), data={'cash_value': .5})
        self.assertEqual(response.status_code, HTTP_200_OK)
        content = response.json()
        self.assertEqual(content, {
            'cash_amount': [2, .5],
            'total_value': 2.5
        })

    def test_insert_invalid_cash(self):
        response = self.client.post(path=reverse(viewname='currency-api'),
                                    data={'cash_value': 3})

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        content = response.content.decode()
        self.assertEqual(content,
                         'Cash value is 3.0 and should be one of (0.01, 0.05, 0.1, 0.25, 0.5, 2, 5, 10)')


class RetrieveCashEndpointTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        repository.retrieve_cash()

    def test_retrieve_cash(self):
        repository.insert_cash(cash=Cash(2))
        repository.insert_cash(cash=Cash(.01))
        repository.insert_cash(cash=Cash(.5))

        response = self.client.delete(path=reverse(viewname='currency-api'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        content = response.json()
        self.assertEqual(content, {
            'cash_amount': [2, .5, .01],
            'total_value': 2.51
        })
