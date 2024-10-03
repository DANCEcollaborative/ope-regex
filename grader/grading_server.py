import json
import requests
import os
import grading_pb2
import grading_pb2_grpc
import local_grader
import grading_utils
from concurrent import futures
import logging
import grpc
import utils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class LocalGradingService(grading_pb2_grpc.GraderServicer):
  def __init__(self) -> None:
    super().__init__()
    self.localGrader = local_grader.LocalGrader()
    self.ope_session_name = os.getenv("OPE_SESSION_NAME")
    self.namespace = os.getenv("OPE_SESSION_NAMESPACE")

  def Grade(self, request, context):
    task = request.task
    logger.debug(f'[DEBUG][LocalGradingService]: Call Grade {task}')
    code = grading_utils.extract_task_n_code(f'workspace/workspace.ipynb', task)
    try:
      fn = grading_utils.string_to_function(code, task)
    except Exception as e:
      return grading_pb2.Response(response=f'Error in grading_server.py: {str(e)}')
    pass_task, feedback = self.localGrader.grade(task, fn)
    logger.debug(f'[DEBUG][LocalGradingService]: result is {pass_task}. Feedback is {feedback}')
    if pass_task:
      logger.debug(f'[DEBUG][LocalGradingService-->Proxy]: Call Complete {self.ope_session_name}/{task}')
      utils.complete(session_name=self.ope_session_name, task=task)
    return grading_pb2.Response(response=feedback)

  def Submit(self, request, context):
    url = f'https://ope.sailplatform.org/api/v1/getSubmissionInfo/{self.namespace}/{self.ope_session_name}'
    response = requests.get(url)
    participantList = json.loads(response.content.decode('utf-8'))
    resp = ''
    for participant in participantList:
      submission_username = participant.get('email', '')
      submission_password = participant.get('password', '')
      postQuizToken = participant.get('postQuizToken', '')
      logger.debug(f'[DEBUG][Submission]: Submit {submission_username}/{submission_password}')
      self.localGrader.submit(submission_username, submission_password)
      resp += f'Post Quiz Token for {submission_username} is {postQuizToken}\n'
    return grading_pb2.Response(response=resp)

  def Release(self, request, context):
    task = request.task
    logger.debug(f'[DEBUG][LocalGradingService]: call release {task}')
    grading_utils.release(task=task)
    resp = f'Released {task}.'
    return grading_pb2.Response(response=resp)


def serve():
  logger.debug(f'[DEBUG][LocalGradingService]: Start')
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  grading_pb2_grpc.add_GraderServicer_to_server(LocalGradingService(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()


if __name__ == '__main__':
  serve()
