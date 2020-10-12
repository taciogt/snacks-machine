from .entities import Cash, CashAmount
from .repositories import CashRepository


def insert_cash(cash: Cash, repository: CashRepository) -> CashAmount:
    repository.insert_cash(cash)
    return repository.get_wallet_cash()


def retrieve_cash(repository: CashRepository) -> CashAmount:
    return repository.retrieve_wallet_cash()


def make_purchase(price: float, repository: CashRepository) -> CashAmount:
    cash_on_wallet = repository.retrieve_wallet_cash()
    repository.insert_cash_on_register(cash_amount=cash_on_wallet)
    return CashAmount()


def calculate_change(price: float, cash_provided: CashAmount, cash_repository: CashRepository) -> CashAmount:
    change = cash_provided - price
    return change
