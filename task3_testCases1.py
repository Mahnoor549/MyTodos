
import unittest
import csv
import customtkinter
import pytest
from unittest.mock import patch, MagicMock

# Stop the GUI event loop while importing the app
original_mainloop = customtkinter.CTk.mainloop
customtkinter.CTk.mainloop = lambda self, *args, **kwargs: None

import mytodos

customtkinter.CTk.mainloop = original_mainloop


def read_test_data():
    data = {}
    with open("test_data.csv", newline="", encoding="utf-8-sig") as file:
        for row in csv.DictReader(file):
            data[row["data_id"]] = row
    return data


data = read_test_data()

@pytest.mark.todo
class TodoManagementTests(unittest.TestCase):

    def setUp(self):
        mytodos.todos_data = []
    @pytest.mark.order(1)
    @patch("mytodos.save_todos")
    @patch("mytodos.show_progress")
    @patch("mytodos.customtkinter.CTkButton")
    @patch("mytodos.customtkinter.CTkCheckBox")
    @patch("mytodos.create_frame")
    def test_TC01_add_valid_task(
        self, create_frame, checkbox_class, button_class,
        show_progress, save_todos
    ):
        row = data["D01"]
        frame = MagicMock()
        checkbox = MagicMock()

        create_frame.return_value = frame
        checkbox_class.return_value = checkbox
        mytodos.todos_entry = MagicMock()
        mytodos.todos_entry.get.return_value = row["input_value"]

        mytodos.add_todo()

        self.assertEqual(len(mytodos.todos_data), 1)
        self.assertEqual(
            mytodos.todos_data[0][0], row["input_value"]
        )
        checkbox_class.assert_called_once()
        show_progress.assert_called_once()
        save_todos.assert_called_once()
        mytodos.todos_entry.delete.assert_called_once()

    @pytest.mark.order(2)
    @patch("mytodos.CTkMessagebox")
    @patch("mytodos.create_frame")

    def test_TC02_empty_task_is_not_added(
        self, create_frame, messagebox
    ):
        mytodos.todos_entry = MagicMock()
        mytodos.todos_entry.get.return_value = data["D02"]["input_value"]

        mytodos.add_todo()

        self.assertEqual(len(mytodos.todos_data), 0)
        create_frame.assert_not_called()
        messagebox.assert_called_once()

    @pytest.mark.order(3)
    @patch("mytodos.save_todos")
    def test_TC03_edit_existing_task(self, save_todos):
        row = data["D03"]
        checkbox = MagicMock()
        frame = MagicMock()

        mytodos.todos_data = [
            (row["input_value"], checkbox, frame)
        ]

        with patch(
            "mytodos.customtkinter.CTkInputDialog"
        ) as dialog:
            dialog.return_value.get_input.return_value = row["second_value"]

            mytodos.edit_todo(0)

        self.assertEqual(
            mytodos.todos_data[0][0], row["second_value"]
        )
        checkbox.configure.assert_called_once_with(
            text=row["second_value"]
        )
        save_todos.assert_called_once()

    @pytest.mark.order(4)
    @patch("mytodos.save_todos")
    @patch("mytodos.show_progress")
    @patch("mytodos.CTkMessagebox")
    def test_TC04_cancel_remove_task(
        self, messagebox, show_progress, save_todos
    ):
        row = data["D04"]
        checkbox = MagicMock()
        checkbox.get.return_value = 0
        frame = MagicMock()

        mytodos.todos_data = [
            (row["input_value"], checkbox, frame)
        ]
        messagebox.return_value.get.return_value = row["second_value"]

        mytodos.remove_todo(frame)

        self.assertEqual(len(mytodos.todos_data), 1)
        self.assertEqual(
            mytodos.todos_data[0][0], row["input_value"]
        )
        frame.destroy.assert_not_called()
        show_progress.assert_not_called()
        save_todos.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
