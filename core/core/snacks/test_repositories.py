from unittest import TestCase

from .entities import Snack
from .repositories import InMemorySnackRepository


class SnacksRepositoryTests(TestCase):
    snack: Snack
    repository = InMemorySnackRepository()

    def setUp(self) -> None:
        super().setUp()
        self.repository.clear_snacks()
        self.snack_to_insert = Snack(price=1, name='S1')
        self.repository.create_snack(self.snack_to_insert)

    def test_recharge_snacks(self):
        self.repository.recharge_snack(name=self.snack_to_insert.name, quantity=2)

        snacks = self.repository.list_snacks()

        self.assertEqual(len(snacks), 1)
        snack = snacks[0]
        self.assertEqual(snack.name, self.snack_to_insert.name)
        self.assertEqual(snack.price, 1)
        self.assertEqual(snack.available_quantity, 2)

    def test_list_snacks(self):
        snacks = self.repository.list_snacks()
        self.assertTrue(snacks, [self.snack_to_insert])
