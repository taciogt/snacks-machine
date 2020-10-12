from abc import ABCMeta, abstractmethod

from core.currency.entities import Cash, CashAmount
from .exceptions import InvalidCashValueError


class CashRepository(metaclass=ABCMeta):
    _VALID_CASH_VALUES = (.01, .05, .10, .25, .50, 2, 5, 10)

    @classmethod
    @abstractmethod
    def _insert_wallet_cash(cls, cash: Cash) -> None:
        ...

    def insert_wallet_cash(self, cash: Cash) -> None:
        if cash.value not in self._VALID_CASH_VALUES:
            raise InvalidCashValueError(invalid_value=cash.value, valid_values=self._VALID_CASH_VALUES)
        self._insert_wallet_cash(cash=cash)

    @classmethod
    @abstractmethod
    def get_wallet_cash(cls) -> CashAmount:
        ...

    @classmethod
    @abstractmethod
    def retrieve_wallet_cash(cls) -> CashAmount:
        ...

    @classmethod
    @abstractmethod
    def insert_cash_on_register(cls, cash_amount: CashAmount) -> None:
        ...

    @classmethod
    @abstractmethod
    def get_cash_available_on_register(cls) -> CashAmount:
        ...

    @classmethod
    @abstractmethod
    def retrieve_cash_available_on_register(cls) -> CashAmount:
        ...


class InMemoryCashRepository(CashRepository):
    _inserted_cash_amount = CashAmount()
    _cash_register = CashAmount()

    @classmethod
    def _insert_wallet_cash(cls, cash: Cash):
        cls._inserted_cash_amount += cash

    @classmethod
    def get_wallet_cash(cls) -> CashAmount:
        return cls._inserted_cash_amount

    @classmethod
    def retrieve_wallet_cash(cls) -> CashAmount:
        cash_to_retrieve = cls._inserted_cash_amount
        cls._inserted_cash_amount = CashAmount()
        return cash_to_retrieve

    @classmethod
    def insert_cash_on_register(cls, cash_amount: CashAmount) -> None:
        cls._cash_register += cash_amount

    @classmethod
    def get_cash_available_on_register(cls) -> CashAmount:
        return cls._cash_register

    @classmethod
    def retrieve_cash_available_on_register(cls) -> CashAmount:
        cash_to_retrieve = cls._cash_register
        cls._cash_register = CashAmount()
        return cash_to_retrieve
