from test_utility import *
import numpy as np
# import openai
import random
import re 
import inspect

task_id = 1

positive_test_cases=['2 hours','4-5 hours','1 hour','2-3 hours','1 HOUR','24 hours']
negative_test_cases=['Overnight','Hour','two']

def solution(x):
	return np.cumsum(x) / (1 + np.arange(len(x)))


def compare_answers(student_out, expected_out):
	return all(np.asarray(student_out) == np.asarray(expected_out))


def test_task(student_solution):
    return True, "Code update is being used"
	# return generate_simple_feedback(student_solution,positive_test_cases,negative_test_cases)

	# return_feedback(student_solution,positive_test_cases,negative_test_cases,NAME)

	# np.random.seed(0)
	# x = np.random.randint(low = 0, high = 10, size = 1000000).astype(float)
	# pass2, feedback2 = test_correctness_and_efficiency(
	# 	cumulative_avg, solution, compare_answers,
	# 	2, f"Input: x = {x}", 10.0, x
	# )

	# if pass1 and pass2:
	# 	record_success(task_id)
	# else:
	# 	record_fail(task_id)

	# record_end(task_id)
	# return pass1 and pass2, feedback1 + "\n" + feedback2






def build_prompt (string,student_name):
    return [
                {"role": "system", "content": "You are a friendly and helpful python tutor. "},
                {"role": "user", "content": f'''Give the student a small hint: speak directly to the student, 
                whose name is {student_name}.  Explain step by step, but don't give the solution away. '''},
                {"role": "assistant", "content":string},
            ]


def generate_simple_feedback(compiled_expression,positive_test_cases,negative_test_cases):
    
    # status_string = f'''The student entered '{compiled_expression.pattern}'.'''

    #tudents_expression = re.compile(expression)
    pos_match=True
    neg_match=False
    
    unmatched=[]
    incorrectly_matched=[]
    # check correctness 
    for pos_example in positive_test_cases:
        if not(compiled_expression.match(pos_example)):
            pos_match=False
            unmatched.append(pos_example)
            
    for neg_example in negative_test_cases:
        if compiled_expression.match(neg_example):
            neg_match=True
            incorrectly_matched.append(neg_example)
            
    if pos_match and not(neg_match):
        return(True, "Congratulations! You have correctly completed the regular expression.")
    elif pos_match and neg_match:
        return(False, f"The student matches too many things. For example you matched {random.choice(incorrectly_matched)} but should not have.")
    elif not pos_match:
        return(False, f"The student does not match the positive cases. For example you did not match {random.choice(unmatched)}.")




def generate_feedback_expression_string(compiled_expression,positive_test_cases,negative_test_cases):
    
    status_string = f'''The student entered '{compiled_expression.pattern}'.'''

    #tudents_expression = re.compile(expression)
    pos_match=True
    neg_match=False
    
    unmatched=[]
    incorrectly_matched=[]
    # check correctness 
    for pos_example in positive_test_cases:
        if not(compiled_expression.match(pos_example)):
            pos_match=False
            unmatched.append(pos_example)
            
    for neg_example in negative_test_cases:
        if compiled_expression.match(neg_example):
            neg_match=True
            incorrectly_matched.append(neg_example)
            
    if pos_match and not(neg_match):
        return(status_string + "The student correctly completed the regular expression. Ask them if there are any alternative solutions which would also work in this case.")
    elif pos_match and neg_match:
        return(status_string + f"The student matches too many things, for example they matched {random.choice(incorrectly_matched)} but should not have.")
    elif not pos_match:
        return(status_string + f"The student does not match the positive cases, for example they do not match {random.choice(unmatched)}.")
    

def test_feedback():
    compiled_regex = re.compile(r'overight')
    student_name = 'Vicente'
    # these would be hidden from the student
    positive_test_cases=['overnight']
    negative_test_cases=['Overnight','overn','night','goodnight','over night']

    return(return_feedback(compiled_regex,positive_test_cases,negative_test_cases,student_name))

def test_split_function(split_recipes):
    
    feedback_prompt=[f'The student wrote this function {inspect.getsource(split_recipes)} '
        ' to split a file up by individual recipes.']
    is_Correct=True
    
    with open('recipe_test_file.txt', 'r') as file:
        test_string = file.read()

    strings_to_evaluate = split_recipes(test_string)

    # make sure you are splitting
    if len(strings_to_evaluate)==1:
        feedback_prompt.append('The function only returned one string, make sure you are using the right method to split.')
        is_Correct = False
    elif len(strings_to_evaluate)==4:
        feedback_prompt.append('The function got the correct number of recipes.')
    else:
        feedback_prompt.append('The function returned an incorrect number of recipes.')
        is_Correct = False
    # make sure you don't lose the recipe
    for recipe in strings_to_evaluate:
        if re.search("Recipe",recipe):
            pass
        else:
            feedback_prompt.append('The recipe does not start with recipe, did you remove it when you split?')
            is_Correct = False
    
    if re.search('browned.$',strings_to_evaluate[0]):
        feedback_prompt.append('The first recipe includes the correct ending.')
        is_Correct = True
    else:
        feedback_prompt.append('The end of the first recipe is not correct.')
        is_Correct = False

    if is_Correct:
        feedback_prompt.append("The student's solution is correct. Ask them to write their own test(s)")

    return is_Correct,' '.join(feedback_prompt)

def return_feedback(compiled_regex,positive_test_cases,negative_test_cases,student_name):
    prompt_string = generate_feedback_expression_string(compiled_regex,positive_test_cases,negative_test_cases)
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=build_prompt(prompt_string,student_name)
    )
    llm_response = response.choices[0].message.content
    return llm_response

def return_feedback_split(split_recipes,NAME):
    is_correct,prompt_string = test_split_function(split_recipes)
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=build_prompt(prompt_string,NAME)
    )
 
    llm_response = response.choices[0].message.content
    return llm_response


