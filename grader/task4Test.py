from test_utility import *
from datetime import datetime
import traceback
import numpy as np

task_id = 4

def solution(X):
	m, n = X.shape
	mask = np.add.outer(np.arange(m), np.arange(n)) % 3 == 0
	return (X * mask).sum()


def compare_answers(student_out, expected_out):
	return student_out == expected_out


def test_task(subset_sum):
	np.random.seed(333)

	X = np.random.randint(low = 1, high = 10, size = (3, 5)).astype(float)
	pass1, feedback1 = test_correctness_and_efficiency(
		subset_sum, solution, compare_answers,
		1, f"Input: X = {X}", 0.0, X
	)

	X = np.random.randint(low = 1, high = 20, size = (1000, 5000)).astype(float)
	pass2, feedback2 = test_correctness_and_efficiency(
		subset_sum, solution, compare_answers,
		2, f"Input: X = {X}", 4.0, X
	)

	if pass1 and pass2:
		record_success(task_id)
	else:
		record_fail(task_id)

	record_end(task_id)
	return pass1 and pass2, feedback1 + "\n" + feedback2


