from unittest import TestCase

from .entities import Cash, CashAmount
from .exceptions import CashUnavailableToSubtractError, NegativeCashAmountError, InvalidCashValueError
from .repositories import InMemoryCashRepository
from .services import calculate_change, insert_cash


class InsertCashTests(TestCase):
    repository = InMemoryCashRepository()

    def test_insert_valid_cash(self):
        insert_cash(Cash(2), repository=self.repository)
        inserted_amount = self.repository.get_wallet_cash()
        self.assertEqual(inserted_amount, CashAmount(2))

    def test_insert_invalid_cash(self):
        self.assertRaisesRegex(InvalidCashValueError,
                               r'Cash value is 1 and should be one of \(0.01, 0.05, 0.1, 0.25, 0.5, 2, 5, 10\)',
                               insert_cash, cash=Cash(1), repository=self.repository)


class RetrieveCashTests(TestCase):
    repository = InMemoryCashRepository()

    def setUp(self) -> None:
        super().setUp()
        self.repository.retrieve_wallet_cash()

    def test_retrieve_cash(self):
        self.repository.insert_cash(cash=Cash(2))
        self.assertEqual(self.repository.retrieve_wallet_cash(), CashAmount(2))
        self.assertEqual(self.repository.get_wallet_cash(), CashAmount())

        self.repository.insert_cash(cash=Cash(2))
        self.repository.insert_cash(cash=Cash(5))
        self.assertEqual(self.repository.retrieve_wallet_cash(), CashAmount(5, 2))
        self.assertEqual(self.repository.get_wallet_cash(), CashAmount())


class CalculateChangeTests(TestCase):
    cash_repository = InMemoryCashRepository()

    def test_change_for_exact_amount(self):
        change = calculate_change(price=1, cash_provided=CashAmount(1), cash_repository=InMemoryCashRepository())
        self.assertEqual(change.total_value, 0)

    def test_change_for_insufficient_amount(self):
        self.assertRaises(NegativeCashAmountError,
                          calculate_change, price=2, cash_provided=CashAmount(1),
                          cash_repository=InMemoryCashRepository())

    def test_change_for_surplus_amount(self):
        change = calculate_change(price=1, cash_provided=CashAmount(1, 1, 1), cash_repository=InMemoryCashRepository())
        self.assertEqual(change, CashAmount(1, 1))

        change = calculate_change(price=2, cash_provided=CashAmount(1, 1, 1), cash_repository=InMemoryCashRepository())
        self.assertEqual(change, CashAmount(1))

        change = calculate_change(price=6, cash_provided=CashAmount(5, 2, 1), cash_repository=InMemoryCashRepository())
        self.assertEqual(change, CashAmount(2))

    def test_change_when_theres_no_exact_coins_or_bills_available(self):
        # TODO: raises an exception specific for change calculation
        self.assertRaisesRegex(CashUnavailableToSubtractError, 'Exact cash not available to subtract',
                               calculate_change, price=1, cash_provided=CashAmount(2),
                               cash_repository=InMemoryCashRepository())
