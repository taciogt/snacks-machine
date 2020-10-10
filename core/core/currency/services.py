from .entities import CashAmount, CashRepository


def calculate_change(price: float, cash_provided: CashAmount, cash_repository: CashRepository) -> CashAmount:
    if price == cash_provided.total_value:
        return CashAmount()
