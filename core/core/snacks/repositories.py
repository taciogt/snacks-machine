from abc import ABCMeta, abstractmethod
from typing import List

from .entities import Snack


class SnackRepository(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def list_snacks(cls) -> List[Snack]:
        ...

    @classmethod
    @abstractmethod
    def create_snack(cls, snack: Snack) -> Snack:
        ...

    @classmethod
    @abstractmethod
    def recharge_snack(cls, name: str, quantity: int) -> Snack:
        ...


class InMemorySnackRepository(SnackRepository):
    snacks: List[Snack] = list()

    @classmethod
    def list_snacks(cls) -> List[Snack]:
        return cls.snacks

    @classmethod
    def create_snack(cls, snack: Snack) -> Snack:
        cls.snacks.append(snack)
        return snack

    @classmethod
    def recharge_snack(cls, name: str, quantity: int) -> Snack:
        snack = next(snack for snack in cls.snacks if snack.name == name)
        snack.available_quantity += quantity
        return snack

    @classmethod
    def clear_snacks(cls):
        cls.snacks = list()
