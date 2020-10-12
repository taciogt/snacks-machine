from dataclasses import asdict
from typing import List

from core.snacks.entities import Snack
from core.snacks.repositories import SnackRepository
from .models import SnackModel
from core.snacks.exceptions import SnackNotFound


class DatabaseRepository(SnackRepository):

    @classmethod
    def get_snack(cls, name: str) -> Snack:
        pass

    @classmethod
    def clear_snacks(cls) -> None:
        SnackModel.objects.all().delete()

    @classmethod
    def recharge_snack(cls, name: str, quantity: int) -> Snack:
        try:
            snack = SnackModel.objects.get(name=name)
        except SnackModel.DoesNotExist:
            raise SnackNotFound(name=name)
        else:
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

    @classmethod
    def remove_snack(cls, snack: Snack, quantity: int) -> None:
        pass
