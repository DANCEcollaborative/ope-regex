# grading strategy

each task has

In tasks folder

* taskN.ipynb

In this folder

* taskNTest.py
    tests for task N
* taskN_test_unit_tests.py
    run unit tests for task N

Tasks 1-4 all share

regular expression part (part a)

Task 3 -4 also incorporate

function implementation part (part b)

All four regular expressions are graded the same way.

The additional functions in tasks 3 and 4 are also graded, by a separate grader.

You can think of the tasks as 3a (regex) and 3b (function) and the same for task 4a (regex) and 4b (function).


This makes the first 1/2 of each grader identical (get regex correct first), and also makes the instructions consistent for the students (get the regex correct first).

Notice that the incorrect implementations are intended to test the *feedback* generation, not the completeness of the test cases. For example, there are many ways to split a list, we don't check if they are incorrect, we just return an empty list, as a trivial case that should trigger *some* feedback. 
