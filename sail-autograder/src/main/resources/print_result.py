import os, sys, json
from cryptography.fernet import Fernet

RESULT_ENCRYPT_KEY = b'eGu_wSKEk8KVomhP7snm_T8QHenYCWm9pLFLqtM43l0='

def main():
	task_id = sys.argv[1]

	# print error message when result.json is not found
	if not os.path.isfile("result.json"):
		print((
			"result.json not found. "
			"Please make sure to run the local tests and submit again."))
		return

	# decrypt and read the content of result.json
	with open("result.json", "rb") as f:
		encrypted_result = f.read()
	fernet = Fernet(RESULT_ENCRYPT_KEY)
	result = fernet.decrypt(encrypted_result).decode()
	result = json.loads(result)

	# print the correctness of the current task for recording
	print(result[task_id])


if __name__ == '__main__':
	main()