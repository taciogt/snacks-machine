class NegativeSnackQuantityError(Exception):
    def __init__(self):
        super().__init__(self.__class__.__name__)
