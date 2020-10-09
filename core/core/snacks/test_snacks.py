from unittest import TestCase
from core.snacks.services import can_buy_snack
from core.snacks.entities import Snack
from core.currency.entities import CashAmount


class MyTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.snack = Snack(name='_', price=1.5)

    def test_can_buy_with_exact_amount(self):
        buying_money = CashAmount(1.5)
        self.assertTrue(can_buy_snack(snack=self.snack, cash_amount=buying_money))

    def test_can_buy_with_insufficient_cash(self):
        buying_money = CashAmount(1)
        # TODO: this exception should be InsufficientCashError
        self.assertRaisesRegex(Exception, 'Insufficient cash. Provided: 1. Required: 1.5',
                               can_buy_snack, snack=self.snack, cash_amount=buying_money)

    def test_can_buy_with_surplus_cash(self):
        buying_money = CashAmount(2)
        self.assertTrue(can_buy_snack(snack=self.snack, cash_amount=buying_money))
