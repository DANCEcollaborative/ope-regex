# function to test the test code

#import task1Test
from task5Test import * 
import os

def main():

    # todo check task id is correct

    # TODO add tests on the TYPE Of 
    # task1_correct:
    # should it be a function, or a 
    # compile regular expression object?
    print(os.getcwd())
    print("This is the main function.")
    simple_feedback = test_task(task5_correct)
    if simple_feedback[0]:
        print('correct solution passed test')
    else:
        print('correct solution failed test (incorrectly)')
    print('tested with correct solution:')
    print(simple_feedback)
    simple_feedback = test_task(task5_incorrect)
    print('tested with incorrect solution:')
    print(simple_feedback)

    if not(simple_feedback[0]):
        print('incorrect solution failed test (as it should)')
    else:
        print('incorrect solution passed test (missed0)')
    

if __name__ == "__main__":
    main()