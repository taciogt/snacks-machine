

class InsufficientCashError(Exception):
    def __init__(self, cash_provided: float, cash_required: float):
        super().__init__(f'Insufficient cash. Provided: R$ {cash_provided:.2f}. Required: R$ {cash_required:.2f}')
