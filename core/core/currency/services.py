from .entities import Cash, CashAmount
from .repositories import CashRepository


def insert_cash(cash: Cash, repository: CashRepository) -> CashAmount:
    repository.insert_cash(cash)
    return repository.get_inserted_cash()


def calculate_change(price: float, cash_provided: CashAmount, cash_repository: CashRepository) -> CashAmount:
    change = cash_provided - price
    return change
