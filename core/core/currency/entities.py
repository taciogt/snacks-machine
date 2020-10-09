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
        return reduce(lambda x, y: x+y, [cash.value for cash in self.cash_items])
