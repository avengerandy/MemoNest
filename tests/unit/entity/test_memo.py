import datetime
import unittest
from dataclasses import FrozenInstanceError

from src.entity.memo import Memo


class TestMemo(unittest.TestCase):
    update_date = datetime.datetime.now() + datetime.timedelta(days=1)
    create_date = datetime.datetime.now()
    id = 1

    def setUp(self):
        self.memo = Memo(title="Example Memo")

    def test_memo_creation(self):
        self.assertEqual(self.memo.title, "Example Memo")

    def test_default_dates(self):
        self.assertIsNone(self.memo.create_date)
        self.assertIsNone(self.memo.update_date)

    def test_is_create(self):
        self.assertIsNone(self.memo.id)
        self.assertFalse(self.memo.is_create())

        memo_with_id = Memo(title="Memo with ID", id=TestMemo.id)
        self.assertTrue(memo_with_id.is_create())

    def test_immutable_memo(self):
        with self.assertRaises(FrozenInstanceError):
            self.memo.title = "New Title"

    def test_complete_memo_attributes(self):
        memo_complete = Memo(
            title="Complete Memo",
            create_date=TestMemo.create_date,
            update_date=TestMemo.update_date,
            id=TestMemo.id,
        )
        self.assertEqual(memo_complete.title, "Complete Memo")
        self.assertEqual(memo_complete.create_date, TestMemo.create_date)
        self.assertEqual(memo_complete.update_date, TestMemo.update_date)
        self.assertEqual(memo_complete.id, TestMemo.id)


if __name__ == "__main__":
    unittest.main()
