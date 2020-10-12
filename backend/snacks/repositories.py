from typing import List

from core.snacks.entities import Snack
from core.snacks.repositories import SnackRepository
from .models import SnackModel


class DatabaseRepository(SnackRepository):
    @classmethod
    def recharge_snack(cls, name: str, quantity: int) -> Snack:
        pass

    @classmethod
    def create_snack(cls, snack: Snack) -> Snack:
        # stored_snack =
        pass

    @classmethod
    def list_snacks(cls) -> List[Snack]:
        snacks = SnackModel.objects.all()
        return [Snack(**snack.as_dict()) for snack in snacks]
