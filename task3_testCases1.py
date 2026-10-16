
import unittest
import csv
from unittest.mock import patch, MagicMock
import customtkinter

# Prevent application GUI from opening during import
original_mainloop = customtkinter.CTk.mainloop
customtkinter.CTk.mainloop = lambda self, *args, **kwargs: None

import mytodos

customtkinter.CTk.mainloop = original_mainloop


# Read test data from CSV
def read_test_data():
    data = {}

    with open("test_data.csv", "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            data[row["data_id"]] = row

    return data

data = read_test_data()



class TodoManagementTests(unittest.TestCase):

    def setUp(self):
        mytodos.todos_data = []

    # TC01: Add a valid task
    def test_TC01_add_valid_task(self):
        task = data["D01"]["input_value"]
        expected = data["D01"]["expected_result"]

        self.assertEqual(task, "Complete assignment")
        self.assertEqual(expected, "Task is added")

    # TC02: Add an empty task
    def test_TC02_add_empty_task(self):
        task = data["D02"]["input_value"]
        expected = data["D02"]["expected_result"]

        self.assertEqual(task, "")
        self.assertEqual(expected, "Task is not added")

    # TC03: Edit an existing task
    def test_TC03_edit_existing_task(self):
        old_task = data["D03"]["input_value"]
        new_task = data["D03"]["second_value"]
        expected = data["D03"]["expected_result"]

        self.assertEqual(old_task, "Old task")
        self.assertEqual(new_task, "Study Python")
        self.assertEqual(expected, "Task text becomes Study Python")

    # TC04: Choose No when removing an incomplete task
    @patch("mytodos.CTkMessagebox")
    def test_TC04_remove_task_choose_no(self, messagebox):
        frame = MagicMock()
        checkbox = MagicMock()
        checkbox.get.return_value = 0

        mytodos.todos_data = [
            (data["D04"]["input_value"], checkbox, frame)
        ]

        messagebox.return_value.get.return_value = (
            data["D04"]["second_value"]
        )

        mytodos.remove_todo(frame)

        self.assertEqual(len(mytodos.todos_data), 1)
        self.assertEqual(
            mytodos.todos_data[0][0],
            "Incomplete task"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
