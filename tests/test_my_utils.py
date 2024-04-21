import unittest
from unittest.mock import MagicMock

from tests.database_mock import SessionLocal


class TestMyUtils(unittest.TestCase):
    def setUp(self):
        # Configure the mock objects
        self.update = MagicMock()
        self.db = SessionLocal()
        # self.db = MagicMock()

    def test_check_valid_chat(self):
        pass
        # Create a MyUtils instance
        # utils = MyUtils()

        # Simulate a valid chat
        # self.update.message.chat_id = 123
        # self.assertTrue(utils.check_valid_chat(self.update))

        # Simulate an invalid chat
        # self.update.message.chat_id = -456
        # self.assertFalse(utils.check_valid_chat(self.update))

        # Simulate an error
        # self.update.message.chat_id = -123
        # with self.assertRaises(Exception):
        #     utils.check_valid_chat(self.update)

    def test_other_method(self):
        pass


if __name__ == "__main__":
    unittest.main()
