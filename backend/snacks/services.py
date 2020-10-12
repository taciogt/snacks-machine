from .repositories import DatabaseRepository
from core.snacks.services import list_snacks as _list_snacks, recharge_snack as _recharge_snack
from core.utils.functions import currying_repository


repository = DatabaseRepository()

list_snacks = currying_repository(_list_snacks, repository=repository)
recharge_snack = currying_repository(_recharge_snack, repository=repository)
