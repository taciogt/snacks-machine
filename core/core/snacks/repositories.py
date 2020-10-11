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
    def insert_snack(cls, snack: Snack) -> Snack:
        ...


class InMemorySnackRepository(SnackRepository):
    snacks: List[Snack] = list()

    @classmethod
    def list_snacks(cls) -> List[Snack]:
        return cls.snacks

    @classmethod
    def insert_snack(cls, snack: Snack) -> Snack:
        cls.snacks.append(snack)
        return snack

