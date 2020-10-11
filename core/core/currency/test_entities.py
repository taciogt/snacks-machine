from unittest import TestCase

from .entities import Cash, CashAmount
from .exceptions import CashUnavailableToSubtractError, NegativeCashAmountError


class CashAmountAddTestCase(TestCase):

    def test_add_cash_to_empty_amount(self):
        self.assertEqual(CashAmount() + Cash(1), CashAmount(1))

    def test_add_cash_to_not_empty_amount(self):
        self.assertEqual(CashAmount(5, 1) + Cash(2), CashAmount(5, 2, 1))

    def test_add_cash_amount_to_empty_amount(self):
        self.assertEqual(CashAmount() + CashAmount(1), CashAmount(1))

    def test_add_cash_amount_to_not_empty_amount(self):
        self.assertEqual(CashAmount(5, 1) + CashAmount(2), CashAmount(5, 2, 1))


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
        self.assertRaises(NegativeCashAmountError,
                          lambda: CashAmount(2, 1) - CashAmount(5))

        self.assertRaises(NegativeCashAmountError,
                          lambda: CashAmount(2, 1) - 5)

    def test_subtract_invalid_type(self):
        self.assertRaisesRegex(TypeError, 'other must be CashAmount or float',
                               lambda: CashAmount(2, 1) - 'invalid_type')

    def test_subtract_when_theres_no_exact_coins_or_bills_available(self):
        self.assertRaisesRegex(CashUnavailableToSubtractError, 'Exact cash not available to subtract',
                               lambda: CashAmount(2) - 1)
