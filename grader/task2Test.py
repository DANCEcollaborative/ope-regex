from test_utility import *
from datetime import datetime
import traceback
import numpy as np

task_id = 2

def solution(x, y):
	alt_plus_minus = np.resize([1, -1], len(x))
	return (x * y).dot(alt_plus_minus)


def compare_answers(student_out, expected_out):
	return student_out == expected_out


def test_task(alt_sum):
	np.random.seed(270)

	x, y = np.random.randint(low = 1, high = 10, size = (2, 10))
	x, y = x.astype(float), y.astype(float)
	pass1, feedback1 = test_correctness_and_efficiency(
		alt_sum, solution, compare_answers,
		1, f"Input: x = {x}, y = {y}", 0.0, x, y
	)

	x, y = np.random.randint(low = 15, high = 30, size = (2, 100000))
	x, y = x.astype(float), y.astype(float)
	pass2, feedback2 = test_correctness_and_efficiency(
		alt_sum, solution, compare_answers,
		2, f"Input: x = {x}, y = {y}", 4.0, x, y)

	if pass1 and pass2:
		record_success(task_id)
	else:
		record_fail(task_id)

	record_end(task_id)
	return pass1 and pass2, feedback1 + "\n" + feedback2


