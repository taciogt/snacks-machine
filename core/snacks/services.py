from snacks.entities import Snack
from currency.exceptions import InsufficientCashError
from currency.entities import CashAmount


def can_buy_snack(snack: Snack, cash_amount: CashAmount):
    if snack.price > cash_amount.total_value:
        raise InsufficientCashError(cash_provided=cash_amount.total_value, cash_required=snack.price)
    return True
