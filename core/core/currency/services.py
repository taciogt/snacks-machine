from .entities import Cash, CashAmount, CashRepository


def insert_cash(cash: Cash, repository: CashRepository):
    repository.insert_cash(cash)


def calculate_change(price: float, cash_provided: CashAmount, cash_repository: CashRepository) -> CashAmount:
    change = cash_provided - price
    return change
