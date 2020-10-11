from unittest import TestCase

from .entities import CashAmount
from .exceptions import CashAmountSubtractionError


class CashAmountSubtractionTestCase(TestCase):

    def test_subtract_empty_amount(self):
        self.assertEqual(CashAmount(1, 1) - CashAmount(), CashAmount(1, 1))

    def test_subtract_same_values(self):
        self.assertEqual(CashAmount(1, 1) - CashAmount(1, 1), CashAmount())
        self.assertEqual(CashAmount(1, 1, 1) - CashAmount(1, 1), CashAmount(1))

    def test_subtract_different_values(self):
        self.assertEqual(CashAmount(2, 1) - CashAmount(2), CashAmount(1))
        self.assertEqual(CashAmount(2, 1, 2) - CashAmount(1, 2, 2), CashAmount())
        self.assertEqual(CashAmount(5, 2, 2, 1) - CashAmount(1, 2), CashAmount(2, 5))
        self.assertEqual(CashAmount(1, 1, 2, 1, 1) - CashAmount(1, 1, 2), CashAmount(1, 1))

    def test_subtract_greater_amount(self):
        self.assertRaisesRegex(CashAmountSubtractionError, 'Not enough cash to subtract',
                               lambda: CashAmount(2, 1) - CashAmount(5))
