import os, json, time
import traceback
from datetime import datetime
import numpy as np
from cryptography.fernet import Fernet

RESULT_ENCRYPT_KEY = b'eGu_wSKEk8KVomhP7snm_T8QHenYCWm9pLFLqtM43l0='
TASK_ENCRYPT_KEY = "8D8C368627985BE"
fernet = Fernet(RESULT_ENCRYPT_KEY)

def test_correctness_and_efficiency(student_fn, solution_fn, compare_answers_fn,
									case_id, input_str, factor, *inp):
	"""
	Test the student's code on correctness and efficiency.

	args:
		student_fn (function): the student's implementation of the task
		solution_fn (function): the reference implementation of the task
		compare_answers_fn (function) : a function returning a boolean
			to indicate whether the student's output matches the expected output
		case_id (int) : the id of the current test case
		input_str (str) : a string that displays the input data to student_fn and solution_fn
		factor (float) : if factor > 0, the runtime of student_fn must be below
			factor * (the runtime of solution_fn) to pass the efficiency check
		inp (Tuple) : the input data to student_fn and solution_fn

	return:
		Tuple[passed, feedback]:
			passed (bool) : whether the student passed this test case
			feedback (str) : the entire feedback string
	"""
	feedback = f"*** Feedback for test case {case_id} *** \n"

	try:
		feedback += input_str + "\n"
		start = datetime.now()
		student_out = student_fn(*inp)
		end = datetime.now()
		student_duration = (end - start).total_seconds()

		start = datetime.now()
		expected_out = solution_fn(*inp)
		end = datetime.now()
		solution_duration = (end - start).total_seconds()

		correctness = compare_answers_fn(student_out, expected_out)
		efficiency = student_duration < factor * solution_duration if factor > 0 else True
		feedback += f"[Runtime Report] Your code took {student_duration} seconds to finish this test case.\n"
	except:
		feedback += "[Exception] Exception thrown while testing -- see the stack trace below:\n\n"
		feedback += traceback.format_exc() + "\n"
		feedback += "[Test Result] You have failed this test case.\n"
		return False, feedback

	if type(student_out) != type(expected_out):
		feedback += (
			f"[Error] Your code's output has type {type(student_out)} "
			f"while the expected output type is {type(expected_out)}.\n"
		)
		correctness = False

	feedback += generate_detailed_feedback(
		correctness, efficiency, student_out, expected_out, solution_duration
	)

	return correctness and efficiency, feedback

def generate_detailed_feedback(	correctness, efficiency, 
							student_out, expected_out, solution_duration):
	"""
	Generate additional feedback for the correctness check and efficiency check.
	"""
	feedback = ""
	
	if correctness:
		feedback += "[Correctness Check] Your code's output is correct.\n"
	else:
		feedback += (
			"[Correctness Check] "
			f"Incorrect output. Your output is {student_out} "
			f"while the reference output is {expected_out}. "
			"Please double check your implementation.\n"
		)

	if efficiency:
		feedback += "[Efficiency Check] Your code is sufficiently fast.\n"
	else:
		feedback += (
			"[Efficiency Check] "
			"Your code is not fast enough. "
			"Please optimize it further and rerun the test. "
			f"For reference, the solution code takes {solution_duration} second(s).\n"
		)

	if correctness and efficiency:
		feedback += "[Test Result] You have passed this test case.\n"
	else:
		feedback += "[Test Result] You have failed this test case.\n"
	return feedback

def record_success(task_id):
	"""
	Record the success of a task at the current timestamp for the OPE bot.
	"""
	ts = time.gmtime()
	t = time.strftime("%a %d %b %Y %H:%M:%S %Z", ts)
	result = json.dumps({"Timestamp" : t, "Testcase" : task_id, "Pass" : "true", "Milestone" : task_id})
	with open("tests.json", "a+") as f:
		f.write(result + os.linesep)

def record_fail(task_id):
	"""
	Record the failure of a task at the current timestamp for the OPE bot.
	"""
	ts = time.gmtime()
	t = time.strftime("%a %d %b %Y %H:%M:%S %Z", ts)
	result = json.dumps({"Timestamp" : t, "Testcase" : task_id, "Milestone" : task_id})
	with open("tests.json", "a+") as f:
	    f.write(result + os.linesep)

def record_end(task_id):
	"""
	Record that the grading of a task has concluded at the current timestamp for the OPE but. 
	"""
	ts = time.gmtime()
	t = time.strftime("%a %d %b %Y %H:%M:%S %Z", ts)
	result = json.dumps({"Timestamp" : t, "End" : "true", "Milestone" : task_id})
	with open("tests.json", "a+") as f:
	    f.write(result + os.linesep)

def write_encrypted_result(result, filename):
	"""
	Write the result JSON to an encrypted file
	"""
	result = json.dumps(result)
	encrypted_result = fernet.encrypt(result.encode())
	with open(filename, "wb") as f:
		f.write(encrypted_result)

def write_result(result, filename):
	"""
	Write the result JSON 
	"""
	result = json.dumps(result)
	with open(filename, "w") as f:
		f.write(result)

