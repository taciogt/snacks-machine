

class InsufficientCashError(Exception):
    def __init__(self, cash_provided: float, cash_required: float):
        super().__init__(f'Insufficient cash. Provided: {cash_provided}. Required: {cash_required}')
