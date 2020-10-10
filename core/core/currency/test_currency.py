from unittest import TestCase
from .services import calculate_change
from .entities import CashAmount, CashRepository


class CashRepositoryMock(CashRepository):
    pass


class CalculateChangeTestCase(TestCase):
    def test_change_for_exact_amount(self):
        price = 1
        cash_amount = CashAmount(1)
        cash_repository = CashRepositoryMock()
        change = calculate_change(price=price, cash_provided=cash_amount, cash_repository=cash_repository)

        self.assertEqual(change.total_value, 0)

