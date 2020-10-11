from unittest import TestCase
from .services import calculate_change
from .entities import CashAmount, CashRepository
from .exceptions import InsufficientCashError, CashUnavailableToSubtractError, NegativeCashAmountError


class CashRepositoryMock(CashRepository):
    pass


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
