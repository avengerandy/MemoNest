import datetime
import unittest
from dataclasses import FrozenInstanceError

from src.entity.memo import Memo, MemoStatusEnum


class TestMemo(unittest.TestCase):
    due_date = datetime.datetime.now() + datetime.timedelta(days=2)
    update_date = datetime.datetime.now() + datetime.timedelta(days=1)
    create_date = datetime.datetime.now()
    total_pomodoros = 5
    now_pomodoros = 2
    id = 1

    def setUp(self):
        self.memo = Memo(
            title="Example Memo",
            description="An example memo description.",
            due_date=TestMemo.due_date,
            status=MemoStatusEnum.TODO,
            total_pomodoros=TestMemo.total_pomodoros,
            now_pomodoros=TestMemo.now_pomodoros,
        )

    def test_memo_creation(self):
        self.assertEqual(self.memo.title, "Example Memo")
        self.assertEqual(self.memo.description, "An example memo description.")
        self.assertEqual(self.memo.due_date, TestMemo.due_date)
        self.assertEqual(self.memo.status, MemoStatusEnum.TODO)
        self.assertEqual(self.memo.total_pomodoros, TestMemo.total_pomodoros)
        self.assertEqual(self.memo.now_pomodoros, TestMemo.now_pomodoros)

    def test_default_dates(self):
        self.assertIsNone(self.memo.create_date)
        self.assertIsNone(self.memo.update_date)

    def test_is_create(self):
        self.assertIsNone(self.memo.id)
        self.assertFalse(self.memo.is_create())

        memo_with_id = Memo(
            title="Memo with ID",
            description="Another memo description.",
            due_date=TestMemo.due_date,
            status=MemoStatusEnum.DOING,
            total_pomodoros=TestMemo.total_pomodoros,
            now_pomodoros=TestMemo.now_pomodoros,
            id=TestMemo.id,
        )
        self.assertTrue(memo_with_id.is_create())

    def test_immutable_memo(self):
        with self.assertRaises(FrozenInstanceError):
            self.memo.title = "New Title"
        with self.assertRaises(FrozenInstanceError):
            self.memo.status = MemoStatusEnum.DOING

    def test_different_statuses(self):
        memo_todo = Memo(
            title="To Do Memo",
            description="Memo that needs to be done.",
            due_date=TestMemo.due_date,
            status=MemoStatusEnum.TODO,
            total_pomodoros=TestMemo.total_pomodoros,
            now_pomodoros=TestMemo.now_pomodoros,
        )
        self.assertEqual(memo_todo.status, MemoStatusEnum.TODO)

        memo_doing = Memo(
            title="Doing Memo",
            description="Memo currently being worked on.",
            due_date=TestMemo.due_date,
            status=MemoStatusEnum.DOING,
            total_pomodoros=TestMemo.total_pomodoros,
            now_pomodoros=TestMemo.now_pomodoros,
        )
        self.assertEqual(memo_doing.status, MemoStatusEnum.DOING)

        memo_done = Memo(
            title="Done Memo",
            description="Memo that is completed.",
            due_date=TestMemo.due_date,
            status=MemoStatusEnum.DONE,
            total_pomodoros=TestMemo.total_pomodoros,
            now_pomodoros=TestMemo.now_pomodoros,
        )
        self.assertEqual(memo_done.status, MemoStatusEnum.DONE)

        with self.assertRaises(ValueError):
            Memo(
                title="Invalid Status Memo",
                description="This memo should raise an error.",
                due_date=TestMemo.due_date,
                status=MemoStatusEnum("invalid_status"),  # Invalid status
                total_pomodoros=TestMemo.total_pomodoros,
                now_pomodoros=TestMemo.now_pomodoros,
            )

    def test_complete_memo_attributes(self):
        memo_complete = Memo(
            title="Complete Memo",
            description="This memo has all attributes set.",
            due_date=TestMemo.due_date,
            total_pomodoros=TestMemo.total_pomodoros,
            now_pomodoros=TestMemo.now_pomodoros,
            status=MemoStatusEnum.TODO,
            create_date=TestMemo.create_date,
            update_date=TestMemo.update_date,
            id=TestMemo.id,
        )
        self.assertEqual(memo_complete.title, "Complete Memo")
        self.assertEqual(memo_complete.description, "This memo has all attributes set.")
        self.assertEqual(memo_complete.due_date, TestMemo.due_date)
        self.assertEqual(memo_complete.total_pomodoros, TestMemo.total_pomodoros)
        self.assertEqual(memo_complete.now_pomodoros, TestMemo.now_pomodoros)
        self.assertEqual(memo_complete.status, MemoStatusEnum.TODO)
        self.assertEqual(memo_complete.create_date, TestMemo.create_date)
        self.assertEqual(memo_complete.update_date, TestMemo.update_date)
        self.assertEqual(memo_complete.id, TestMemo.id)


class TestMemoStatusEnum(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(MemoStatusEnum.TODO.value, "todo")
        self.assertEqual(MemoStatusEnum.DOING.value, "doing")
        self.assertEqual(MemoStatusEnum.DONE.value, "done")

    def test_invalid_enum_value(self):
        with self.assertRaises(ValueError):
            MemoStatusEnum("invalid_status")


if __name__ == "__main__":
    unittest.main()
