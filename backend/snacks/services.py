from typing import List
from core.snacks.entities import Snack
from .repositories import DatabaseRepository
from core.snacks.services import list_snacks as core_list_snacks


def list_snacks() -> List[Snack]:
    return core_list_snacks(repository=DatabaseRepository())
