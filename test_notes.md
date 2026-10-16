ECP and BVA Test Notes

1. Todo Management Module

Functions: add_todo(), edit_todo(), remove_todo()

ECP

Test Input	     Equivalence Class	Expected Result
Empty task name	        Invalid input	Task should not be added
Non-empty task name	Valid input	Task should be added
Normal task name with 
letters and numbers	Valid input	Task should be added
Editing with a new 
non-empty name	        Valid input	Task name should be updated
Editing with empty 
input	               Invalid input	Existing task name should remain unchanged

BVA — Boundary Value Analysis

Task Name Length	      Expected Result
0 characters	         Task should not be added
1 character	         Task should be added
Multiple characters	 Task should be added

2.File Handling Module

Functions: save_todos(), load_todos()

ECP 
Test Condition	         Expected Result
File exists and 
contains tasks	            Tasks should load correctly
File does not exist	    Application should handle the missing file
File contains an empty 
task list	            No tasks should load
File contains completed
and incomplete tasks	    Task names and completion states should be restored

BVA 

Number of Saved Tasks	           Expected Result
0 tasks	                       Empty list should be handled
1 task	                       One task should load correctly
Multiple tasks	               All saved tasks should load correctly

3. Progress Tracking Module

Function: show_progress()

ECP 
Test Condition	               Expected Result
No tasks exist	               Progress should show 0 of 0 done
Tasks exist but
none are completed	       Progress should show 0 completed
Some tasks are completed.      Progress should show the correct completed count
All tasks are completed	       Progress should show all tasks as done

BVA 
Total Tasks	Completed Tasks	Expected Progress
0	0	0 of 0 done
1	0	0 of 1 done
1	1	1 of 1 done
2	1	1 of 2 done
2	2	2 of 2 done

Conclusion
ECP and BVA were used to identify valid, invalid, and boundary test conditions for Todo Management, File Handling, and Progress Tracking. These notes will be used to design automated unit test cases for the MyTodos application.