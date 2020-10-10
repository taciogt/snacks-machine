from dataclasses import dataclass
from typing import List
from functools import reduce


@dataclass
class Cash:
    value: float


class CashAmount:
    cash_items: List[Cash]

    def __init__(self, *args):
        self.cash_items = [Cash(value=value) for value in args]

    @property
    def total_value(self):
        return reduce(lambda x, y: x+y, [cash.value for cash in self.cash_items], 0)

    @property
    def _cash_values(self):
        return [cash.value for cash in self.cash_items]

    def __str__(self):
        return f'CashAmount(R$ {self.total_value:.2f})={self._cash_values}'

    __repr__ = __str__


class CashRepository:
    pass
