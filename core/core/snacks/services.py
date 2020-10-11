from typing import List

from core.currency.entities import CashAmount
from core.currency.exceptions import InsufficientCashError
from .entities import Snack
from .repositories import SnackRepository


def can_buy_snack(snack: Snack, cash_amount: CashAmount):
    if snack.price > cash_amount.total_value:
        raise InsufficientCashError(cash_provided=cash_amount.total_value, cash_required=snack.price)
    return True


def list_snacks(repository: SnackRepository) -> List[Snack]:
    return repository.list_snacks()
