# function to test the test code

#import task1Test
from task1Test import * 

def main():

    # TODO add tests on the TYPE Of 
    # task1_correct:
    # should it be a function, or a 
    # compile regular expression object?

    print("This is the main function.")
    simple_feedback = test_task(task1_correct_regex)
    print('tested with correct solution:')
    print(simple_feedback)
    simple_feedback = test_task(task1_incorrect_regex)
    print('tested with incorrect solution:')
    print(simple_feedback)

if __name__ == "__main__":
    main()