# function to test the test code

#import task1Test
from task3Test import * 
import os

def main():

    # todo check task id is correct

    # TODO add tests on the TYPE Of 
    # task1_correct:
    # should it be a function, or a 
    # compile regular expression object?
    print(os.getcwd())
    print("This is the main function.")
    simple_feedback = test_task3a(task3a_correct())
    if simple_feedback[0]:
        print('correct solution passed test')
    else:
        print('correct solution failed test (incorrectly)')
    print('tested with correct solution:')
    print(simple_feedback)
    simple_feedback = test_task3a(task3a_incorrect())
    print('tested with incorrect solution:')
    print(simple_feedback)

    if not(simple_feedback[0]):
        print('incorrect solution failed test (as it should)')
    else:
        print('incorrect solution passed test (missed0)')
    
    task_feedback = test_split_function(task_3b_incorrect)
    print('tested with incorrect solution:')
    print(simple_feedback)
    

if __name__ == "__main__":
    main()
