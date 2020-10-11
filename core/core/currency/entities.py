from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from typing import List
from .exceptions import CashAmountSubtractionError


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

    def add_cash(self, cash: Cash):
        self._cash_items.append(cash)
        self._sort_cash_items()

    def __sub__(self, other: CashAmount) -> CashAmount:
        other_index = 0
        other_len = len(other._cash_items)

        new_amount = CashAmount()
        for cash in self._cash_items:
            if other_index < other_len and cash == other._cash_items[other_index]:
                other_index += 1
            else:
                new_amount.add_cash(cash)

        if other_index < other_len:
            raise CashAmountSubtractionError(original_cash_value=self.total_value, subtraction_value=other.total_value)

        return new_amount

    @property
    def _cash_values(self):
        return [cash.value for cash in self._cash_items]

    def _sort_cash_items(self):
        self._cash_items = sorted(self._cash_items, key=lambda cash: cash.value)

    def __str__(self):
        return f'CashAmount(R$ {self.total_value:.2f})={self._cash_values}'

    __repr__ = __str__

    def __eq__(self, other):
        return self._cash_items == other._cash_items


class CashRepository:
    pass
