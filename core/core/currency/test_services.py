from unittest import TestCase

from .entities import Cash, CashAmount, CashRepository
from .exceptions import CashUnavailableToSubtractError, NegativeCashAmountError
from .services import calculate_change, insert_cash


class CashRepositoryMock(CashRepository):
    _inserted_cash_amount = CashAmount()

    def insert_cash(self, cash: Cash):
        self._inserted_cash_amount.add_cash(cash)

    def get_inserted_cash(self) -> CashAmount:
        return self._inserted_cash_amount


class InsertCashTestCase(TestCase):
    repository = CashRepositoryMock()

    def test_insert_valid_cash(self):
        insert_cash(Cash(1), repository=self.repository)
        inserted_amount = self.repository.get_inserted_cash()
        self.assertEqual(inserted_amount, CashAmount(1))


class CalculateChangeTestCase(TestCase):
    cash_repository = CashRepositoryMock()

    def test_change_for_exact_amount(self):
        change = calculate_change(price=1, cash_provided=CashAmount(1), cash_repository=CashRepositoryMock())
        self.assertEqual(change.total_value, 0)

    def test_change_for_insufficient_amount(self):
        self.assertRaises(NegativeCashAmountError,
                          calculate_change, price=2, cash_provided=CashAmount(1),
                          cash_repository=CashRepositoryMock())

    def test_change_for_surplus_amount(self):
        change = calculate_change(price=1, cash_provided=CashAmount(1, 1, 1), cash_repository=CashRepositoryMock())
        self.assertEqual(change, CashAmount(1, 1))

        change = calculate_change(price=2, cash_provided=CashAmount(1, 1, 1), cash_repository=CashRepositoryMock())
        self.assertEqual(change, CashAmount(1))

        change = calculate_change(price=6, cash_provided=CashAmount(5, 2, 1), cash_repository=CashRepositoryMock())
        self.assertEqual(change, CashAmount(2))

    def test_change_when_theres_no_exact_coins_or_bills_available(self):
        # TODO: raises an exception specific for change calculation
        self.assertRaisesRegex(CashUnavailableToSubtractError, 'Exact cash not available to subtract',
                               calculate_change, price=1, cash_provided=CashAmount(2),
                               cash_repository=CashRepositoryMock())
