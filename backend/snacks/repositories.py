from dataclasses import asdict
from typing import List

from core.snacks.entities import Snack
from core.snacks.exceptions import SnackNotFound
from core.snacks.repositories import SnackRepository
from .models import SnackModel


class DatabaseRepository(SnackRepository):

    @classmethod
    def _get_snack_model(cls, name: str) -> SnackModel:
        try:
            snack_model: SnackModel = SnackModel.objects.get(name=name)
            return snack_model
        except SnackModel.DoesNotExist:
            raise SnackNotFound(name=name)

    @classmethod
    def get_snack(cls, name: str) -> Snack:
        snack_model = cls._get_snack_model(name=name)
        return Snack(**snack_model.as_dict())

    @classmethod
    def clear_snacks(cls) -> None:
        SnackModel.objects.all().delete()

    @classmethod
    def recharge_snack(cls, name: str, quantity: int) -> Snack:
        snack_model = cls._get_snack_model(name=name)
        snack_model.available_quantity += quantity
        snack_model.save()
        return Snack(**snack_model.as_dict())

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
