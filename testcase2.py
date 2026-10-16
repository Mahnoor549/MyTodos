import customtkinter
import unittest
from unittest.mock import MagicMock, patch, mock_open

# Prevent the app window from blocking the tests
customtkinter.CTk.mainloop = lambda self: None

import mytodos


class TestMyTodosMember2(unittest.TestCase):

    def setUp(self):
        mytodos.todos_data = []
        mytodos.todos_listbox = MagicMock()
        mytodos.progress_button = MagicMock()

    @patch("mytodos.customtkinter.CTkFrame")
    def test_create_frame_returns_frame(self, mock_frame):
        expected_frame = MagicMock()
        mock_frame.return_value = expected_frame

        result = mytodos.create_frame()

        self.assertIs(result, expected_frame)

    @patch("mytodos.customtkinter.CTkFrame")
    def test_create_frame_called_once(self, mock_frame):
        mytodos.create_frame()

        mock_frame.assert_called_once()

    @patch("mytodos.customtkinter.CTkFrame")
    def test_create_frame_uses_todos_listbox(self, mock_frame):
        mytodos.create_frame()

        args, kwargs = mock_frame.call_args
        self.assertTrue(
            mytodos.todos_listbox in args
            or kwargs.get("master") is mytodos.todos_listbox
        )

    @patch("mytodos.customtkinter.CTkFrame")
    def test_create_frame_grid_called(self, mock_frame):
        mytodos.create_frame()

        mock_frame.return_value.grid.assert_called_once()

    @patch("mytodos.customtkinter.CTkFrame")
    def test_create_two_frames(self, mock_frame):
        first = mytodos.create_frame()
        second = mytodos.create_frame()

        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        self.assertEqual(mock_frame.call_count, 2)

    @patch("mytodos.pickle.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_empty_list(self, mock_file, mock_dump):
        mytodos.todos_data = []

        mytodos.save_todos()

        mock_dump.assert_called_once_with([], mock_file())

    @patch("mytodos.pickle.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_one_todo(self, mock_file, mock_dump):
        checkbox = MagicMock()
        checkbox.get.return_value = 0
        mytodos.todos_data = [("Study", checkbox, MagicMock())]

        mytodos.save_todos()

        saved = mock_dump.call_args[0][0]
        self.assertEqual(saved, [("Study", 0)])

    @patch("mytodos.pickle.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_multiple_todos(self, mock_file, mock_dump):
        cb1, cb2 = MagicMock(), MagicMock()
        cb1.get.return_value = 0
        cb2.get.return_value = 1

        mytodos.todos_data = [
            ("Study", cb1, MagicMock()),
            ("Assignment", cb2, MagicMock())
        ]

        mytodos.save_todos()

        saved = mock_dump.call_args[0][0]
        self.assertEqual(len(saved), 2)

    @patch("mytodos.pickle.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_completed_status(self, mock_file, mock_dump):
        checkbox = MagicMock()
        checkbox.get.return_value = 1
        mytodos.todos_data = [("Task A", checkbox, MagicMock())]

        mytodos.save_todos()

        saved = mock_dump.call_args[0][0]
        self.assertEqual(saved[0], ("Task A", 1))

    @patch("mytodos.pickle.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_opens_file_for_writing(self, mock_file, mock_dump):
        mytodos.todos_data = []

        mytodos.save_todos()

        mock_file.assert_called_once_with("todos.txt", "wb")

    @patch("mytodos.os.path.exists", return_value=False)
    def test_load_missing_file(self, mock_exists):
        mytodos.todos_data = []

        mytodos.load_todos()

        self.assertEqual(mytodos.todos_data, [])

    @patch("mytodos.create_frame")
    @patch("mytodos.customtkinter.CTkCheckBox")
    @patch("builtins.open", new_callable=mock_open)
    @patch("mytodos.pickle.load", return_value=[])
    @patch("mytodos.os.path.exists", return_value=True)
    def test_load_empty_file(self, mock_exists, mock_load, mock_file,
                             mock_checkbox, mock_frame):
        mytodos.todos_data = []

        mytodos.load_todos()

        self.assertEqual(mytodos.todos_data, [])

    @patch("mytodos.create_frame")
    @patch("mytodos.customtkinter.CTkCheckBox")
    @patch("mytodos.customtkinter.CTkButton")
    @patch("builtins.open", new_callable=mock_open)
    @patch("mytodos.pickle.load", return_value=[("Study", 0)])
    @patch("mytodos.os.path.exists", return_value=True)
    def test_load_one_todo(self, mock_exists, mock_load, mock_file,
                           mock_button, mock_checkbox, mock_frame):
        mytodos.todos_data = []

        mytodos.load_todos()

        self.assertEqual(len(mytodos.todos_data), 1)
        self.assertEqual(mytodos.todos_data[0][0], "Study")

    @patch("mytodos.create_frame")
    @patch("mytodos.customtkinter.CTkCheckBox")
    @patch("mytodos.customtkinter.CTkButton")
    @patch("builtins.open", new_callable=mock_open)
    @patch("mytodos.pickle.load", return_value=[("Study", 0), ("Task B", 1)])
    @patch("mytodos.os.path.exists", return_value=True)
    def test_load_multiple_todos(self, mock_exists, mock_load, mock_file,
                                 mock_button, mock_checkbox, mock_frame):
        mytodos.todos_data = []

        mytodos.load_todos()

        self.assertEqual(len(mytodos.todos_data), 2)

    @patch("mytodos.create_frame")
    @patch("mytodos.customtkinter.CTkCheckBox")
    @patch("mytodos.customtkinter.CTkButton")
    @patch("builtins.open", new_callable=mock_open)
    @patch("mytodos.pickle.load", return_value=[("Finished task", 1)])
    @patch("mytodos.os.path.exists", return_value=True)
    def test_load_completed_todo(self, mock_exists, mock_load, mock_file,
                                 mock_button, mock_checkbox, mock_frame):
        mytodos.todos_data = []

        mytodos.load_todos()

        self.assertEqual(mytodos.todos_data[0][0], "Finished task")
        mock_checkbox.return_value.select.assert_called()

    def test_progress_empty_list(self):
        mytodos.todos_data = []

        mytodos.show_progress()

        mytodos.progress_button.configure.assert_called_with(
            text="0 of 0 done"
        )

    def test_progress_one_incomplete(self):
        cb = MagicMock()
        cb.get.return_value = 0
        mytodos.todos_data = [("Study", cb, MagicMock())]

        mytodos.show_progress()

        mytodos.progress_button.configure.assert_called_with(
            text="0 of 1 done"
        )

    def test_progress_one_completed(self):
        cb = MagicMock()
        cb.get.return_value = 1
        mytodos.todos_data = [("Study", cb, MagicMock())]

        mytodos.show_progress()

        mytodos.progress_button.configure.assert_called_with(
            text="1 of 1 done"
        )

    def test_progress_mixed_tasks(self):
        cb1, cb2, cb3 = MagicMock(), MagicMock(), MagicMock()
        cb1.get.return_value = 1
        cb2.get.return_value = 0
        cb3.get.return_value = 1

        mytodos.todos_data = [
            ("A", cb1, MagicMock()),
            ("B", cb2, MagicMock()),
            ("C", cb3, MagicMock())
        ]

        mytodos.show_progress()

        mytodos.progress_button.configure.assert_called_with(
            text="2 of 3 done"
        )

    def test_progress_all_completed(self):
        cb1, cb2 = MagicMock(), MagicMock()
        cb1.get.return_value = 1
        cb2.get.return_value = 1

        mytodos.todos_data = [
            ("A", cb1, MagicMock()),
            ("B", cb2, MagicMock())
        ]

        mytodos.show_progress()

        mytodos.progress_button.configure.assert_called_with(
            text="2 of 2 done"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)