import unittest
from core.snacks.services import buy_snack
from core.snacks.entities import Snack
from core.currency.entities import Cash, CashAmount


class MyTestCase(unittest.TestCase):
    def test_buy_with_exact_amount(self):
        snack = Snack(name='-', value=1.5)
        buying_money = CashAmount(1, 0.5)
        self.assertTrue(buy_snack(snack=snack, cash_amount=buying_money))
