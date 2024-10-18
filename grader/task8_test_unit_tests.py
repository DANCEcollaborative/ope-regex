# function to test the test code

#import task1Test
from task8Test import * 

def main():

    # TODO add tests on the TYPE Of 
    # task1_correct:
    # should it be a function, or a 
    # compile regular expression object?

    print("This is the main function.")

    
    print('tested with correct solution:')
    simple_feedback = test_task(task8_correct)
    print(simple_feedback)
    
    print('tested with incorrect solution:')
    simple_feedback = test_task(task8_incorrect)
    print(simple_feedback)
   
if __name__ == "__main__":
    main()