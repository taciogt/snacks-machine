from typing import List

from core.currency.entities import CashAmount
from core.currency.exceptions import InsufficientCashError
from core.currency.repositories import CashRepository
from core.currency.services import make_purchase
from .entities import Snack
from .exceptions import NegativeSnackQuantityError
from .repositories import SnackRepository


def can_buy_snack(snack: Snack, cash_amount: CashAmount):
    if snack.price > cash_amount.total_value:
        raise InsufficientCashError(cash_provided=cash_amount.total_value, cash_required=snack.price)
    return True


def buy_snack(name: str, repository: SnackRepository, cash_repository: CashRepository) -> CashAmount:
    snack = repository.get_snack(name=name)
    change = make_purchase(price=snack.price, repository=cash_repository)
    repository.remove_snack(snack=snack, quantity=1)
    return change


def list_snacks(repository: SnackRepository) -> List[Snack]:
    return repository.list_snacks()


def recharge_snack(name: str, quantity: int, repository: SnackRepository) -> Snack:
    if quantity < 0:
        raise NegativeSnackQuantityError
    return repository.recharge_snack(name=name, quantity=quantity)
