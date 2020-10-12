class NegativeSnackQuantityError(Exception):
    def __init__(self):
        super().__init__(self.__class__.__name__)


class SnackNotFound(Exception):
    def __init__(self, name):
        super().__init__(f'Snack "{name}" not found.')
