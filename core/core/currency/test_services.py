from unittest import TestCase
from .services import calculate_change
from .entities import CashAmount, CashRepository
from .exceptions import InsufficientCashError


class CashRepositoryMock(CashRepository):
    pass


class CalculateChangeTestCase(TestCase):
    cash_repository = CashRepositoryMock()

    def test_change_for_exact_amount(self):
        change = calculate_change(price=1, cash_provided=CashAmount(1), cash_repository=CashRepositoryMock())
        self.assertEqual(change.total_value, 0)

    def test_change_for_insufficient_amount(self):
        self.assertRaisesRegex(InsufficientCashError, r'Insufficient cash. Provided: R\$ 1.00. Required: R\$ 2.00',
                               calculate_change, price=2, cash_provided=CashAmount(1),
                               cash_repository=CashRepositoryMock())

    # def test_change_for_surplus_amount(self):
    #     change = calculate_change(price=1, cash_provided=CashAmount(1, 1, 1), cash_repository=CashRepositoryMock())
    #     self.assertEqual(change, CashAmount(1, 1))
