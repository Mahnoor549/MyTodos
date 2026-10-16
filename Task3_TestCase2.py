import unittest
import csv
import os
import tempfile
import customtkinter
from unittest.mock import patch, MagicMock

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


class ProgressTrackingTests(unittest.TestCase):

    def setUp(self):
        mytodos.todos_data = []
        mytodos.progress_button = MagicMock()

    def test_TC05_progress_empty(self):
        expected = data["D05"]["expected_result"]

        mytodos.show_progress()

        mytodos.progress_button.configure.assert_called_once_with(
            text=expected
        )

    def test_TC06_progress_incomplete(self):
        row = data["D06"]
        checkbox = MagicMock()
        checkbox.get.return_value = int(row["second_value"])

        mytodos.todos_data = [
            (row["input_value"], checkbox, MagicMock())
        ]

        mytodos.show_progress()

        mytodos.progress_button.configure.assert_called_once_with(
            text=row["expected_result"]
        )

    def test_TC07_progress_completed(self):
        row = data["D07"]
        checkbox = MagicMock()
        checkbox.get.return_value = int(row["second_value"])

        mytodos.todos_data = [
            (row["input_value"], checkbox, MagicMock())
        ]

        mytodos.show_progress()

        mytodos.progress_button.configure.assert_called_once_with(
            text=row["expected_result"]
        )


class FileHandlingTests(unittest.TestCase):

    def setUp(self):
        mytodos.todos_data = []

    def test_TC08_save_and_load_task(self):
        row = data["D08"]
        old_directory = os.getcwd()

        try:
            with tempfile.TemporaryDirectory() as temp_directory:
                os.chdir(temp_directory)

                # Test actual save_todos() using a mock checkbox
                checkbox = MagicMock()
                checkbox.get.return_value = int(row["second_value"])

                mytodos.todos_data = [
                    (row["input_value"], checkbox, MagicMock())
                ]

                mytodos.save_todos()

                self.assertTrue(os.path.exists("todos.txt"))

                # Check the saved contents by loading through
                # the actual application function
                mytodos.todos_data = []
                frame = MagicMock()

                with patch(
                    "mytodos.create_frame", return_value=frame
                ), patch(
                    "mytodos.customtkinter.CTkCheckBox"
                ) as checkbox_class, patch(
                    "mytodos.customtkinter.CTkButton"
                ):
                    loaded_checkbox = MagicMock()
                    checkbox_class.return_value = loaded_checkbox

                    mytodos.load_todos()

                self.assertEqual(len(mytodos.todos_data), 1)
                self.assertEqual(
                    mytodos.todos_data[0][0], row["input_value"]
                )
                loaded_checkbox.select.assert_called_once()

        finally:
            os.chdir(old_directory)


if __name__ == "__main__":
    unittest.main(verbosity=2)