
import random
import re 
import inspect

# this is a stub of a function-tester

# task_id = 
task_id = 2

def task2_correct(x):
    integer_hour_pattern = re.compile(r'(?<!\S)\d{1,2}(?:-\d{1,2})?\s*hours?\b', re.IGNORECASE)
    #integer_hour_pattern = re.compile(r'hours?', re.IGNORECASE)
    matches = integer_hour_pattern.findall(x)
    return matches 

def task2_incorrect(x):

    integer_hour_pattern = re.compile(r'2 Hours', re.IGNORECASE)
    matches = integer_hour_pattern.findall(x)
    print(matches)
    return matches 


def task1b_incorrect_ii(x):

    integer_hour_pattern = re.compile(r'5 hours', re.IGNORECASE)
    matches = integer_hour_pattern.findall(x)
    print(matches)
    return matches 

# you shouldn't need to modify this
def test_task(student_solution):
    student_result = student_solution()
    return generate_simple_feedback(student_result)

# def generate_simple_feedback(student_result,test_input):
def generate_simple_feedback(student_result):
    '''
    notice that the feedback is a tuple 
    telling us if they passed or failed the test(s)
    and generating some simple feedback if they failed

    '''
    
    matches = student_result
    pos_examples=['2 HOURS', '4-5 hours']
    neg_examples=['5 hours','5 Hours']
    return test_matches(matches,pos_examples,neg_examples)


def test_matches(matches,pos_examples,neg_examples):
    #
    # this is an example of code written to test a 'specific' function
    #
    # you should find ALL of the things in positive match
    # (across the entire document)
    # and none of the things in negative match
    pos_match = set(pos_examples)
    neg_match = set(neg_examples)

    if set(matches)==set(pos_match) and len(set(matches).intersection(set(neg_match)))==0:
        return True,[]
    else:
        incorrectly_matched=set(matches)-set(pos_match)
        #not_detected = set(matches).intersection(neg_match)
        
        overmatches = set(matches).intersection(neg_examples)

        mistakes=[] # list of mismatches
        # note you cannot return False,[]
        # by construction, as an empty list already returns
        for id in incorrectly_matched:
            mistakes.append(f'incorrectly detected: {id}')
        for om in overmatches:
            mistakes.append(f'incorrectly matched: {om}')
        return False,mistakes
        
    
