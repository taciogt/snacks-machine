from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from typing import List, Union

from .exceptions import CashUnavailableToSubtractError, NegativeCashAmountError


@dataclass
class Cash:
    value: float


class CashAmount:
    _cash_items: List[Cash]

    def __init__(self, *args):
        self._cash_items = [Cash(value=value) for value in args]
        self._sort_cash_items()

    @property
    def total_value(self):
        return reduce(lambda x, y: x+y, [cash.value for cash in self._cash_items], 0)

    def __add__(self, other: Union[Cash, CashAmount]) -> CashAmount:
        if isinstance(other, CashAmount):
            amount_to_add = other
        elif isinstance(other, Cash):
            amount_to_add = CashAmount(other.value)
        else:
            raise TypeError(f'other must be {Cash.__name__} but is {other.__class__.__name__}')
        return CashAmount(*self.cash_values, *amount_to_add.cash_values)

    def __sub__(self, other: Union[CashAmount, float]) -> CashAmount:
        if isinstance(other, CashAmount):
            value_to_subtract = other.total_value
        elif isinstance(other, (int, float)):
            value_to_subtract = other
        else:
            raise TypeError(f'other must be {CashAmount.__name__} or {float.__name__}')

        if self.total_value < value_to_subtract:
            raise NegativeCashAmountError()

        new_amount = CashAmount()
        for cash in self._cash_items:
            if cash.value <= value_to_subtract:
                value_to_subtract -= cash.value
            else:
                new_amount += cash
        if value_to_subtract == 0:
            return new_amount
        else:
            raise CashUnavailableToSubtractError()

    @property
    def cash_values(self):
        return [cash.value for cash in self._cash_items]

    def _sort_cash_items(self):
        self._cash_items = sorted(self._cash_items, key=lambda cash: -cash.value)

    def __str__(self):
        return f'CashAmount(R$ {self.total_value:.2f})={self.cash_values}'

    __repr__ = __str__

    def __eq__(self, other):
        return isinstance(other, CashAmount) and \
               self._cash_items == other._cash_items
