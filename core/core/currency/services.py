from .entities import Cash, CashAmount
from .repositories import CashRepository
from .exceptions import InsufficientCashError, CashUnavailableToSubtractError, CashForChangeUnavailable


def insert_cash(cash: Cash, repository: CashRepository) -> CashAmount:
    repository.insert_wallet_cash(cash)
    return repository.get_wallet_cash()


def retrieve_cash(repository: CashRepository) -> CashAmount:
    return repository.retrieve_wallet_cash()


def make_purchase(price: float, repository: CashRepository) -> CashAmount:
    wallet_cash = repository.get_wallet_cash()
    register_cash = repository.get_cash_available_on_register()

    wallet_value = wallet_cash.total_value
    if price > wallet_value:
        raise InsufficientCashError(cash_provided=wallet_value, cash_required=price)

    cash_available = wallet_cash + register_cash
    try:
        change = cash_available - price
    except CashUnavailableToSubtractError:
        raise CashForChangeUnavailable
    else:
        repository.retrieve_wallet_cash()
        repository.retrieve_cash_available_on_register()

        cash_to_insert_on_register = cash_available - change
        repository.insert_cash_on_register(cash_amount=cash_to_insert_on_register)
        return change


def calculate_change(price: float, cash_provided: CashAmount, cash_repository: CashRepository) -> CashAmount:
    change = cash_provided - price
    return change
