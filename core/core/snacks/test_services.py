from unittest import TestCase

from core.currency.entities import CashAmount
from core.currency.exceptions import InsufficientCashError
from .entities import Snack
from .exceptions import NegativeSnackQuantityError
from .repositories import InMemorySnackRepository
from .services import can_buy_snack, recharge_snack, list_snacks


class RechargeSnacksTests(TestCase):
    snack: Snack
    repository = InMemorySnackRepository()

    def setUp(self) -> None:
        super().setUp()
        self.repository.clear_snacks()
        self.snack_to_insert = Snack(price=1, name='S1')
        self.repository.create_snack(self.snack_to_insert)

    def test_recharge_snacks(self):
        recharge_snack(name=self.snack_to_insert.name, quantity=2, repository=self.repository)

        snacks = list_snacks(repository=self.repository)

        self.assertEqual(len(snacks), 1)
        snack = snacks[0]
        self.assertEqual(snack.name, self.snack_to_insert.name)
        self.assertEqual(snack.price, 1)
        self.assertEqual(snack.available_quantity, 2)

    def test_recharge_snacks_with_negative_quantity(self):
        self.assertRaises(NegativeSnackQuantityError,
                          recharge_snack, name=self.snack_to_insert.name, quantity=-1, repository=self.repository)


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