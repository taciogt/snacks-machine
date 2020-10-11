from django.test import Client
from django.test import TestCase
from django.urls import reverse

from web_utils.http_status_codes import HTTP_200_OK


class InsertCashEndpointTests(TestCase):
    def test_insert_cash(self):
        client = Client()
        response = client.post(path=reverse(viewname='currency-api'), data={'cash_value': 2})

        self.assertEqual(response.status_code, HTTP_200_OK)
        content = response.json()
        self.assertEqual(content, {
            'cash_amount': [2],
            'total_value': 2
        })

        response = client.post(path=reverse(viewname='currency-api'), data={'cash_value': .5})
        self.assertEqual(response.status_code, HTTP_200_OK)
        content = response.json()
        self.assertEqual(content, {
            'cash_amount': [2, .5],
            'total_value': 2.5
        })
