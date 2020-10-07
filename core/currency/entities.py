from dataclasses import dataclass
from typing import List


@dataclass
class Cash:
    value: float


class CashAmount:
    values: List[Cash]

    def __init__(self, *args):
        self.values = [Cash(value=value) for value in args]
