from functools import partial

from core.snacks.services import list_snacks as _list_snacks, recharge_snack as _recharge_snack, \
    buy_snack as _buy_snack
from currency.services import repository as cash_repository
from .repositories import DatabaseRepository

repository = DatabaseRepository()

list_snacks = partial(_list_snacks, repository=repository)
recharge_snack = partial(_recharge_snack, repository=repository)
buy_snack = partial(_buy_snack, repository=repository, cash_repository=cash_repository)