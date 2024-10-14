# function to test the test code

#import task1Test
from task1bTest import * 

recipe_text = r'''
Recipe 1: 194_Cabbage_Kielbara_Supper
1) In a 5-qt. slow cooker, combine the cabbage, potatoes, onion, salt and pepper.
2) Pour broth over all for 2 HOURS.
3) Place sausage on top (slow cooker will be full, but cabbage will cook down).
4) Cover and cook on low for 4-5 hours or until vegetables are tender and sausage is heated through.
Recipe 2: 195_Chocolate_Chip_Cookie_Ice_Cream_Cake
1) Crush half the cookies (about 20 cookies) to make crumbs.
2) Combine crumbs with melted margarine and press into the bottom of a 9-inch springform pan or pie plate.
3) Stand remaining cookies around edge of pan.
4) Spread 3/4 cup fudge topping over crust.
5) Freeze 1.5 hours.
6) Meanwhile, soften 1 quart of ice cream in microwave or on countertop.
7) After crust has chilled, spread softened ice cream over fudge layer.
8) Freeze 30 minutes.
9) Scoop remaining quart of ice cream into balls and arrange over spread ice cream layer.
10) Freeze until firm, 3.5-4.5 Hours.
11) To serve, garnish with remainder of fudge topping, whipped cream and cherries.'''


def main():

    # TODO add tests on the TYPE Of 
    # task1_correct:

    # should it be a function, or a 
    # compile regular expression object?
    print('tested with correct solution:')

    simple_feedback = test_task(task1b_correct,recipe_text)
    print(simple_feedback)

    print('tested with incorrect solution:')
    simple_feedback = test_task(task1b_incorrect,recipe_text)

    print(simple_feedback)

    print('tested with incorrect solution:')
    simple_feedback = test_task(task1b_incorrect_ii,recipe_text)

    print(simple_feedback)

if __name__ == "__main__":
    main()
