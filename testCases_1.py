import unittest
from unittest.mock import MagicMock, patch
import customtkinter

customtkinter.CTk.mainloop = lambda self: None
import mytodos


class TestMyTodos(unittest.TestCase):

    def setUp(self):
        mytodos.todos_data = []
        mytodos.todos_entry = MagicMock()
        mytodos.todos_listbox = MagicMock()
        mytodos.progress_button = MagicMock()
        mytodos.show_progress = MagicMock()
        mytodos.save_todos = MagicMock()

    # 1. add_todo() - 5 tests

    @patch("mytodos.customtkinter.CTkButton")
    @patch("mytodos.customtkinter.CTkCheckBox")
    def test_add_normal(self, cb, btn):
        mytodos.todos_entry.get.return_value = "Study"
        mytodos.create_frame = MagicMock()
        mytodos.add_todo()
        self.assertEqual(len(mytodos.todos_data), 1)

    @patch("mytodos.CTkMessagebox")
    def test_add_empty(self, msg):
        mytodos.todos_entry.get.return_value = ""
        mytodos.add_todo()
        self.assertEqual(len(mytodos.todos_data), 0)

    @patch("mytodos.customtkinter.CTkButton")
    @patch("mytodos.customtkinter.CTkCheckBox")
    def test_add_one_letter(self, cb, btn):
        mytodos.todos_entry.get.return_value = "A"
        mytodos.create_frame = MagicMock()
        mytodos.add_todo()
        self.assertEqual(len(mytodos.todos_data), 1)

    @patch("mytodos.customtkinter.CTkButton")
    @patch("mytodos.customtkinter.CTkCheckBox")
    def test_add_numbers(self, cb, btn):
        mytodos.todos_entry.get.return_value = "Task123"
        mytodos.create_frame = MagicMock()
        mytodos.add_todo()
        self.assertEqual(len(mytodos.todos_data), 1)

    @patch("mytodos.customtkinter.CTkButton")
    @patch("mytodos.customtkinter.CTkCheckBox")
    def test_add_spaces(self, cb, btn):
        mytodos.todos_entry.get.return_value = "   "
        mytodos.create_frame = MagicMock()
        mytodos.add_todo()
        self.assertEqual(len(mytodos.todos_data), 1)

    # 2. checked() - 5 tests

    def test_checked(self):
        cb = MagicMock()
        cb.get.return_value = 1
        mytodos.checked(cb)
        mytodos.save_todos.assert_called()

    def test_unchecked(self):
        cb = MagicMock()
        cb.get.return_value = 0
        mytodos.checked(cb)
        mytodos.save_todos.assert_called()

    def test_checked_progress(self):
        cb = MagicMock()
        cb.get.return_value = 1
        mytodos.checked(cb)
        mytodos.show_progress.assert_called()

    def test_unchecked_progress(self):
        cb = MagicMock()
        cb.get.return_value = 0
        mytodos.checked(cb)
        mytodos.show_progress.assert_called()

    def test_checked_font(self):
        cb = MagicMock()
        cb.get.return_value = 1
        mytodos.checked(cb)
        cb.configure.assert_called()

    # 3. edit_todo() - 5 tests

    def set_task(self):
        cb = MagicMock()
        cb.get.return_value = 0
        mytodos.todos_data = [("Old", cb, MagicMock())]

    @patch("mytodos.customtkinter.CTkInputDialog")
    def test_edit_name(self, dialog):
        self.set_task()
        dialog.return_value.get_input.return_value = "New"
        mytodos.edit_todo(0)
        self.assertEqual(mytodos.todos_data[0][0], "New")

    @patch("mytodos.customtkinter.CTkInputDialog")
    def test_edit_empty(self, dialog):
        self.set_task()
        dialog.return_value.get_input.return_value = ""
        mytodos.edit_todo(0)
        self.assertEqual(mytodos.todos_data[0][0], "Old")

    @patch("mytodos.customtkinter.CTkInputDialog")
    def test_edit_cancel(self, dialog):
        self.set_task()
        dialog.return_value.get_input.return_value = None
        mytodos.edit_todo(0)
        self.assertEqual(mytodos.todos_data[0][0], "Old")

    @patch("mytodos.customtkinter.CTkInputDialog")
    def test_edit_numbers(self, dialog):
        self.set_task()
        dialog.return_value.get_input.return_value = "Task123"
        mytodos.edit_todo(0)
        self.assertEqual(mytodos.todos_data[0][0], "Task123")

    @patch("mytodos.customtkinter.CTkInputDialog")
    def test_edit_saves(self, dialog):
        self.set_task()
        dialog.return_value.get_input.return_value = "New"
        mytodos.edit_todo(0)
        mytodos.save_todos.assert_called()

    # 4. remove_todo() - 5 tests

    @patch("mytodos.CTkMessagebox")
    def test_remove_yes(self, msg):
        frame = MagicMock()
        cb = MagicMock()
        cb.get.return_value = 1
        mytodos.todos_data = [("A", cb, frame)]
        msg.return_value.get.return_value = "Yes"
        mytodos.remove_todo(frame)
        self.assertEqual(len(mytodos.todos_data), 0)

    
    @patch("mytodos.CTkMessagebox")
    def test_remove_no(self, msg):
        frame = MagicMock()
        cb = MagicMock()
        cb.get.return_value = 0  # Task is not completed

        mytodos.todos_data = [("A", cb, frame)]
        msg.return_value.get.return_value = "No"

        mytodos.remove_todo(frame)

        self.assertEqual(len(mytodos.todos_data), 1)


    @patch("mytodos.CTkMessagebox")
    def test_remove_second(self, msg):
        cb1, cb2 = MagicMock(), MagicMock()
        cb1.get.return_value = cb2.get.return_value = 1
        f1, f2 = MagicMock(), MagicMock()
        mytodos.todos_data = [("A", cb1, f1), ("B", cb2, f2)]
        msg.return_value.get.return_value = "Yes"
        mytodos.remove_todo(f2)
        self.assertNotIn("B", [x[0] for x in mytodos.todos_data])

    @patch("mytodos.CTkMessagebox")
    def test_remove_completed(self, msg):
        frame = MagicMock()
        cb = MagicMock()
        cb.get.return_value = 1
        mytodos.todos_data = [("A", cb, frame)]
        msg.return_value.get.return_value = "Yes"
        mytodos.remove_todo(frame)
        self.assertEqual(len(mytodos.todos_data), 0)

    def test_remove_empty(self):
        mytodos.todos_data = []
        mytodos.remove_todo(MagicMock())
        self.assertEqual(len(mytodos.todos_data), 0)

    # 5. remove_done_todos() - 5 tests

    @patch("mytodos.CTkMessagebox")
    def test_remove_one_done(self, msg):
        cb = MagicMock()
        cb.get.return_value = 1
        mytodos.todos_data = [("A", cb, MagicMock())]
        mytodos.remove_done_todos()
        self.assertEqual(len(mytodos.todos_data), 0)

    @patch("mytodos.CTkMessagebox")
    def test_remove_some_done(self, msg):
        cb1, cb2 = MagicMock(), MagicMock()
        cb1.get.return_value = 1
        cb2.get.return_value = 0
        mytodos.todos_data = [("A", cb1, MagicMock()),
                              ("B", cb2, MagicMock())]
        mytodos.remove_done_todos()
        self.assertEqual(len(mytodos.todos_data), 1)

    @patch("mytodos.CTkMessagebox")
    def test_remove_none_done(self, msg):
        cb = MagicMock()
        cb.get.return_value = 0
        mytodos.todos_data = [("A", cb, MagicMock())]
        mytodos.remove_done_todos()
        self.assertEqual(len(mytodos.todos_data), 1)

    @patch("mytodos.CTkMessagebox")
    def test_remove_all_done(self, msg):
        cb1, cb2 = MagicMock(), MagicMock()
        cb1.get.return_value = cb2.get.return_value = 1
        mytodos.todos_data = [("A", cb1, MagicMock()),
                              ("B", cb2, MagicMock())]
        mytodos.remove_done_todos()
        self.assertEqual(len(mytodos.todos_data), 0)

    @patch("mytodos.CTkMessagebox")
    def test_remove_done_empty(self, msg):
        mytodos.todos_data = []
        mytodos.remove_done_todos()
        self.assertEqual(len(mytodos.todos_data), 0)


if __name__ == "__main__":
    unittest.main()