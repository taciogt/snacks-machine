from functools import partial

from core.currency.entities import Cash, CashAmount
from core.currency.repositories import InMemoryCashRepository
from core.currency.services import insert_cash as _insert_cash, retrieve_cash as _retrieve_cash

repository = InMemoryCashRepository()


def insert_cash(cash_value: float) -> CashAmount:
    cash_amount = _insert_cash(cash=Cash(cash_value), repository=repository)
    return cash_amount


retrieve_cash = partial(_retrieve_cash, repository=repository)
