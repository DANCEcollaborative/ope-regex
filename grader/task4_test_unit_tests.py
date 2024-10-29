# function to test the test code

#import task1Test
from task4Test import * 


def main():

    # TODO add tests on the TYPE Of 
    # task1_correct:
    # should it be a function, or a 
    # compile regular expression object?

    print("This is the main function.")
    simple_feedback = test_task(task4_correct)
    print('tested with correct solution:')
    print(simple_feedback)

    simple_feedback = test_task(task4_incorrect)
    print('tested with incorrect solution:')
    print(simple_feedback)


if __name__ == "__main__":
    main()