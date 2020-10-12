from abc import ABCMeta, abstractmethod
from typing import List

from .entities import Snack
from .exceptions import SnackNotFound


class SnackRepository(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def list_snacks(cls) -> List[Snack]:
        ...

    @classmethod
    @abstractmethod
    def get_snack(cls, name: str) -> Snack:
        ...

    @classmethod
    @abstractmethod
    def create_snack(cls, snack: Snack) -> Snack:
        ...


    @classmethod
    @abstractmethod
    def recharge_snack(cls, name: str, quantity: int) -> Snack:
        ...

    @classmethod
    @abstractmethod
    def clear_snacks(cls) -> None:
        ...

    @classmethod
    @abstractmethod
    def remove_snack(cls, snack: Snack, quantity: int) -> None:
        ...


class InMemorySnackRepository(SnackRepository):
    snacks: List[Snack] = list()

    @classmethod
    def get_snack(cls, name: str) -> Snack:
        try:
            return next(snack for snack in cls.snacks if snack.name == name)
        except StopIteration:
            raise SnackNotFound(name=name)

    @classmethod
    def list_snacks(cls) -> List[Snack]:
        return cls.snacks

    @classmethod
    def create_snack(cls, snack: Snack) -> Snack:
        cls.snacks.append(snack)
        return snack

    @classmethod
    def recharge_snack(cls, name: str, quantity: int) -> Snack:
        snack = cls.get_snack(name=name)
        snack.available_quantity += quantity
        return snack

    @classmethod
    def clear_snacks(cls):
        cls.snacks = list()

    @classmethod
    def remove_snack(cls, snack: Snack, quantity: int) -> None:
        snack = cls.get_snack(name=snack.name)
        snack.available_quantity -= quantity
