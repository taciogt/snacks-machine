from core.currency.entities import Cash, CashAmount
from core.currency.repositories import InMemoryCashRepository
from core.currency.services import insert_cash as core_insert_cash


def insert_cash(cash_value: float) -> CashAmount:
    cash_amount = core_insert_cash(cash=Cash(cash_value), repository=InMemoryCashRepository())
    return cash_amount
