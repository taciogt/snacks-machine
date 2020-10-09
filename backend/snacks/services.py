# from typing import List
# from core.snacks.entities import Snack
from .models import SnackModel


# def list_snacks() -> List[Snack]:
def list_snacks():
    snacks = SnackModel.objects.all()
    return [snack.as_dict() for snack in snacks]
