from dataclasses import dataclass


@dataclass
class Snack:
    name: str
    price: float
    available_quantity: int = 0
