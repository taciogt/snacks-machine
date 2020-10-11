
class InsufficientCashError(Exception):
    def __init__(self, cash_provided: float, cash_required: float):
        super().__init__(f'Insufficient cash. Provided: R$ {cash_provided:.2f}. Required: R$ {cash_required:.2f}')


class CashAmountSubtractionError(Exception):
    def __init__(self, original_cash_value: float, subtraction_value: float):
        super().__init__('Not enough cash to subtract')


class CashUnavailableToSubtractError(Exception):
    def __init__(self):
        super().__init__('Exact cash not available to subtract')

