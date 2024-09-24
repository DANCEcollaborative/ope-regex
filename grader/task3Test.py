from test_utility import *
from datetime import datetime
import traceback
import numpy as np

task_id = 3

def solution(H, y):
	n = len(y)
	return -np.log(H[np.arange(n), y]).sum() / n


def compare_answers(student_out, expected_out):
	return student_out == expected_out


def test_task(logistic_loss):
	np.random.seed(42)

	H = np.array([[0.1, 0.1, 0.5, 0.2, 0.1], [0.2, 0.2, 0.2, 0.2, 0.2], [0.1, 0.2, 0.3, 0.2, 0.2]])
	y = np.random.choice(np.arange(H.shape[1]), size = H.shape[0])
	pass1, feedback1 = test_correctness_and_efficiency(
		logistic_loss, solution, compare_answers,
		1, f"Input: H = {H}, y = {y}", 0.0, H, y
	)

	H = np.random.randint(low = 1, high = 100, size = (1000, 5)).astype(float)
	H /= H.sum(axis = 1)[:,None]
	y = np.random.choice(np.arange(H.shape[1]), size = H.shape[0])
	pass2, feedback2 = test_correctness_and_efficiency(
		logistic_loss, solution, compare_answers,
		2, f"Input: H = {H}, y = {y}", 20.0, H, y
	)

	if pass1 and pass2:
		record_success(task_id)
	else:
		record_fail(task_id)

	record_end(task_id)
	return pass1 and pass2, feedback1 + "\n" + feedback2



