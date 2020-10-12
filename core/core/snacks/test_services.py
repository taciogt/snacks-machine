from functools import partial
from unittest import TestCase

from core.currency.entities import Cash, CashAmount
from core.currency.services import insert_cash as _insert_cash, retrieve_cash as _retrieve_cash
from core.currency.repositories import InMemoryCashRepository
from core.currency.exceptions import InsufficientCashError
from .entities import Snack
from .exceptions import NegativeSnackQuantityError, SnackNotFound
from .repositories import InMemorySnackRepository
from .services import can_buy_snack, recharge_snack as _recharge_snack, list_snacks as _list_snacks, \
    buy_snack as _buy_snack

cash_repository = InMemoryCashRepository()
insert_cash = partial(_insert_cash, repository=cash_repository)
retrieve_cash = partial(_retrieve_cash, repository=cash_repository)

repository = InMemorySnackRepository()
list_snacks = partial(_list_snacks, repository=repository)
recharge_snack = partial(_recharge_snack, repository=repository)
buy_snack = partial(_buy_snack, repository=repository, cash_repository=cash_repository)


class RechargeSnacksTests(TestCase):
    snack: Snack

    def setUp(self) -> None:
        super().setUp()
        repository.clear_snacks()
        self.snack_to_insert = Snack(price=1, name='S1')
        repository.create_snack(self.snack_to_insert)

    def test_recharge_snacks(self):
        recharge_snack(name=self.snack_to_insert.name, quantity=2)

        snacks = list_snacks()

        self.assertEqual(len(snacks), 1)
        snack = snacks[0]
        self.assertEqual(snack.name, self.snack_to_insert.name)
        self.assertEqual(snack.price, 1)
        self.assertEqual(snack.available_quantity, 2)

    def test_recharge_snacks_with_negative_quantity(self):
        self.assertRaises(NegativeSnackQuantityError,
                          recharge_snack, name=self.snack_to_insert.name, quantity=-1)

    def test_recharge_snacks_with_invalid_name(self):
        self.assertRaisesRegex(SnackNotFound, 'Snack "invalid name" not found.',
                               recharge_snack, name='invalid name', quantity=1)


class BuySnacksTests(TestCase):
    snack: Snack

    def setUp(self) -> None:
        super().setUpClass()
        repository.clear_snacks()
        cash_repository.retrieve_wallet_cash()
        cash_repository.retrieve_cash_available_on_register()

        self.snack = Snack(name='_', price=1.5)

        self.snack_a = Snack(name='snack-a', price=2)
        repository.create_snack(self.snack_a)
        repository.recharge_snack(name=self.snack_a.name, quantity=5)

    # def test_can_buy_with_exact_amount(self):
    #     buying_money = CashAmount(1.5)
    #     self.assertTrue(can_buy_snack(snack=self.snack, cash_amount=buying_money))

    # def test_can_buy_with_insufficient_cash(self):
    #     buying_money = CashAmount(1)
    #     self.assertRaisesRegex(InsufficientCashError, r'Insufficient cash. Provided: R\$ 1.00. Required: R\$ 1.50',
    #                            can_buy_snack, snack=self.snack, cash_amount=buying_money)

    def test_can_buy_with_surplus_cash(self):
        buying_money = CashAmount(2)
        self.assertTrue(can_buy_snack(snack=self.snack, cash_amount=buying_money))

    def test_buy_with_exact_amount(self):
        insert_cash(cash=Cash(2))

        change = buy_snack(name=self.snack_a.name)
        self.assertEqual(change, CashAmount())
        snacks_available = list_snacks()
        self.assertEqual(snacks_available, [Snack(name='snack-a',
                                                  price=2,
                                                  available_quantity=4)])

        self.assertEqual(cash_repository.get_wallet_cash(), CashAmount())
        self.assertEqual(cash_repository.get_cash_available_on_register(), CashAmount(2))

    def test_buy_with_insufficient_cash(self):
        insert_cash(cash=Cash(.5))

        self.assertRaisesRegex(InsufficientCashError, r'Insufficient cash. Provided: R\$ 0.50. Required: R\$ 2.00',
                               buy_snack, name=self.snack_a.name)

        snacks_available = list_snacks()
        self.assertEqual(snacks_available, [Snack(name='snack-a',
                                                  price=2,
                                                  available_quantity=5)])

        self.assertEqual(cash_repository.get_wallet_cash(), CashAmount(.5))
        self.assertEqual(cash_repository.get_cash_available_on_register(), CashAmount())
