import unittest
from core.snacks.services import foo


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(foo(), False)
