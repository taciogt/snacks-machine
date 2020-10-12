from typing import List, NoReturn

from core.snacks.entities import Snack
from core.snacks.repositories import SnackRepository
from .models import SnackModel
from dataclasses import asdict


class DatabaseRepository(SnackRepository):
    @classmethod
    def clear_snacks(cls) -> None:
        SnackModel.objects.all().delete()

    @classmethod
    def recharge_snack(cls, name: str, quantity: int) -> Snack:
        snack = SnackModel.objects.get(name=name)
        snack.available_quantity += quantity
        snack.save()
        return Snack(**snack.as_dict())

    @classmethod
    def create_snack(cls, snack: Snack) -> Snack:
        snack = SnackModel(**asdict(snack))
        snack.save()
        return Snack(**snack.as_dict())

    @classmethod
    def list_snacks(cls) -> List[Snack]:
        snacks = SnackModel.objects.all()
        return [Snack(**snack.as_dict()) for snack in snacks]
