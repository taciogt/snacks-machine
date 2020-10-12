from functools import partial

from core.snacks.services import list_snacks as _list_snacks, recharge_snack as _recharge_snack
from .repositories import DatabaseRepository

repository = DatabaseRepository()

list_snacks = partial(_list_snacks, repository=repository)
recharge_snack = partial(_recharge_snack, repository=repository)
