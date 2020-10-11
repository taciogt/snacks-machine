from unittest import TestCase

from core.currency.entities import CashAmount
from core.currency.exceptions import InsufficientCashError
from .entities import Snack
from .repositories import InMemorySnackRepository
from .services import can_buy_snack
from .exceptions import NegativeSnackQuantityError


class SnacksRepositoryTests(TestCase):
    snack: Snack
    repository = InMemorySnackRepository()

    def setUp(self) -> None:
        super().setUp()
        self.repository.clear_snacks()
        self.snack_to_insert = Snack(price=1, name='S1')
        self.repository.create_snack(self.snack_to_insert)

    def test_recharge_snacks(self):
        self.repository.recharge_snack(name=self.snack_to_insert.name, quantity=2)

        snacks = self.repository.list_snacks()

        self.assertEqual(len(snacks), 1)
        snack = snacks[0]
        self.assertEqual(snack.name, self.snack_to_insert.name)
        self.assertEqual(snack.price, 1)
        self.assertEqual(snack.available_quantity, 2)

    def test_recharge_snacks_with_negative_quantity(self):
        self.assertRaises(NegativeSnackQuantityError,
                          self.repository.recharge_snack, name=self.snack_to_insert.name, quantity=-1)

    def test_list_snacks(self):
        snacks = self.repository.list_snacks()
        self.assertTrue(snacks, [self.snack_to_insert])


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
