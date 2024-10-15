import math
import utils
import task1Test, task2Test, task3Test, task4Test
import submitter_script
from typing import Tuple

class Feedback:
  def __init__(self, score: int, message: str = "") -> None:
    self.message = message
    self.score = score

  def __str__(self) -> str:
    return f"Feedback:\n{self.message}" + f"\n***Final Score***: {self.score}"

class LocalGrader:
  def __init__(self) -> None:
    self.feedbacks = {}
    self.test_function_map = {
      'task1a': task1aTest.test_task,
      'task2': task2Test.test_task,
      'task3': task3Test.test_task,
      'task4': task4Test.test_task
    }
    self.result = {
      task_tag : 0
      for task_tag in self.test_function_map.keys()
    }

  def grade(self, task: str, student_function)-> Tuple[bool, str]:
    if task not in self.test_function_map.keys():
      return False, f"Task does not exist: {task}"
    test_function = self.test_function_map[task]
    passed, feedback_message = test_function(student_function)
    feedback = Feedback(int(passed), feedback_message)
    self.feedbacks[task] = feedback
    self.result[task] = int(passed)
    return passed, str(feedback)

  def submit(self, username: str, password: str)  -> None:
    submitter_script.submit(username, password, self.result)


if __name__ == '__main__':
  grader = LocalGrader()
  for task_tag in grader.test_function_map.keys():
    task_code = utils.extract_task_n_code(f'../tasks/{task_tag}.ipynb', task_tag)
    task_fn = utils.string_to_function(task_code, task_tag)
    passed, task_feedback = grader.grade(task_tag, task_fn)
    print(task_feedback)
        