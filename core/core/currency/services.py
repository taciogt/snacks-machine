from .entities import CashAmount, CashRepository


def calculate_change(price: float, cash_provided: CashAmount, cash_repository: CashRepository) -> CashAmount:
    change = cash_provided - price
    return change
