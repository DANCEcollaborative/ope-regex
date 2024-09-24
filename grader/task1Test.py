from test_utility import *
import numpy as np

task_id = 1

def solution(x):
	return np.cumsum(x) / (1 + np.arange(len(x)))


def compare_answers(student_out, expected_out):
	return all(np.asarray(student_out) == np.asarray(expected_out))


def test_task(cumulative_avg):
	x = np.arange(10).astype(float)
	pass1, feedback1 = test_correctness_and_efficiency(
		cumulative_avg, solution, compare_answers,
		1, f"Input: x = {x}", 0.0, x
	)

	np.random.seed(0)
	x = np.random.randint(low = 0, high = 10, size = 1000000).astype(float)
	pass2, feedback2 = test_correctness_and_efficiency(
		cumulative_avg, solution, compare_answers,
		2, f"Input: x = {x}", 10.0, x
	)

	if pass1 and pass2:
		record_success(task_id)
	else:
		record_fail(task_id)

	record_end(task_id)
	return pass1 and pass2, feedback1 + "\n" + feedback2


