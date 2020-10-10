from .entities import CashAmount, CashRepository
from .exceptions import InsufficientCashError


def calculate_change(price: float, cash_provided: CashAmount, cash_repository: CashRepository) -> CashAmount:
    if price == cash_provided.total_value:
        return CashAmount()
    elif price > cash_provided.total_value:
        raise InsufficientCashError(cash_provided=cash_provided.total_value, cash_required=price)
    else:
        cash_to_pay = CashAmount()
        for cash in cash_provided._cash_items:
            if cash_to_pay.total_value < price:
                cash_to_pay.add_cash(cash)
        return cash_provided - cash_to_pay


