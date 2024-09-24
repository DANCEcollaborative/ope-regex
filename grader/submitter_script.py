import requests, json, os
import tarfile
from operator import itemgetter
from test_utility import write_encrypted_result

# Submission Specific Config
LMS_NAME = "sail2"
PROJECT_ID = "ope-author-practice-xvjlkkm3"
PROJECT_LEARN_ID = "pe-learn-practice-p032vbfd"
TASK_ID = "a6802abd-e9ad-48aa-934c-0b35ce1e320a"
SECRET_KEY = "AK8e97WS3M8ETW6akTBJ9D"
ARTIFACT_VERSION = "v1"
DURATION = 50
COURSE_TYPE = "foundation-data-science"

STUDENT_DNS = requests.get("https://ipinfo.io/ip").text
AGS_DNS = "autograding.sailplatform.org"
SIGNATURE = "1K9SaGliHwthRgeOi12hUdCUwAPmN"

NOTEBOOK_FILENAME = "./workspace/workspace.ipynb"
RESULT_FILENAME = "result.json"


def submit(username, password, result):
	url = f"https://{AGS_DNS}/submit"
	params = {
		"signature" : SIGNATURE,
		"submissionUsername" : username,
		"submissionPassword" : password,
		"dns" : STUDENT_DNS,
		"projectId" : PROJECT_ID,
		"taskId" : TASK_ID,
		"secretKey" : SECRET_KEY,
		"duration" : DURATION,
		"lmsName" : LMS_NAME,
		"courseType" : COURSE_TYPE,
		"artifactVersion" : ARTIFACT_VERSION
	}
	tar_filename = f"{username}.tar.gz"

	# generate the result json file
	write_encrypted_result(result, RESULT_FILENAME)

	# add the result json file and workspace notebook
	# to a submission tar
	with tarfile.open(tar_filename, "w:gz") as tar:
		tar.add(NOTEBOOK_FILENAME)
		tar.add(RESULT_FILENAME)

	# submit the tar to AGS
	with open(tar_filename, "rb") as tar:
		files = {"file" : tar}
		response = requests.post(url, files = files, params = params)
		response_json = json.loads(response.text)
		success, status, message = itemgetter \
			('success', 'status', 'message')(response_json)
		if success:
			print("Your code has been successfully submitted to Sail()")
		else:
			print(f"Submission error, status code: {status}, message: {message}")

	# delete the submission files
	os.remove(RESULT_FILENAME)
	os.remove(tar_filename)

