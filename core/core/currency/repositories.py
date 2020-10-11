from abc import ABCMeta, abstractmethod

from core.currency.entities import Cash, CashAmount
from .exceptions import InvalidCashValueError


class CashRepository(metaclass=ABCMeta):
    _VALID_CASH_VALUES = (.01, .05, .10, .25, .50, 2, 5, 10)

    @classmethod
    @abstractmethod
    def _insert_cash(cls, cash: Cash) -> None:
        ...

    def insert_cash(self, cash: Cash) -> None:
        if cash.value not in self._VALID_CASH_VALUES:
            raise InvalidCashValueError(invalid_value=cash.value, valid_values=self._VALID_CASH_VALUES)
        self._insert_cash(cash=cash)

    @classmethod
    @abstractmethod
    def get_inserted_cash(cls) -> CashAmount:
        ...


class InMemoryCashRepository(CashRepository):
    _inserted_cash_amount = CashAmount()

    @classmethod
    def _insert_cash(cls, cash: Cash):
        cls._inserted_cash_amount += cash

    @classmethod
    def get_inserted_cash(cls) -> CashAmount:
        return cls._inserted_cash_amount