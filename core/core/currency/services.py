from .entities import CashAmount, CashRepository
from .exceptions import InsufficientCashError


def calculate_change(price: float, cash_provided: CashAmount, cash_repository: CashRepository) -> CashAmount:
    if price == cash_provided.total_value:
        return CashAmount()
    else:
        raise InsufficientCashError(cash_provided=cash_provided.total_value, cash_required=price)
