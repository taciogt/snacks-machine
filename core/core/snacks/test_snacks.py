from unittest import TestCase

from core.currency.entities import CashAmount
from core.currency.exceptions import InsufficientCashError
from .entities import Snack
from .repositories import InMemorySnackRepository
from .services import can_buy_snack


class SnacksRepositoryTests(TestCase):
    snack: Snack
    repository = InMemorySnackRepository()

    def test_list_snacks(self):
        snack_to_insert = Snack(price=1, name='S1')
        self.repository.insert_snack(snack_to_insert)

        snacks = self.repository.list_snacks()
        self.assertTrue(snacks, [snack_to_insert])

    def test_recharge_snacks(self):
        pass


class BuySnacksTests(TestCase):
    snack: Snack

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.snack = Snack(name='_', price=1.5)

    def test_can_buy_with_exact_amount(self):
        buying_money = CashAmount(1.5)
        self.assertTrue(can_buy_snack(snack=self.snack, cash_amount=buying_money))

    def test_can_buy_with_insufficient_cash(self):
        buying_money = CashAmount(1)
        self.assertRaisesRegex(InsufficientCashError, r'Insufficient cash. Provided: R\$ 1.00. Required: R\$ 1.50',
                               can_buy_snack, snack=self.snack, cash_amount=buying_money)

    def test_can_buy_with_surplus_cash(self):
        buying_money = CashAmount(2)
        self.assertTrue(can_buy_snack(snack=self.snack, cash_amount=buying_money))
