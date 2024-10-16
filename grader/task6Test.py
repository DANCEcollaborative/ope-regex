
import random
import re 
import inspect

# this is a stub of a function-tester


recipe_text_B = '''
Recipe 1: 183_Armadillo_Eggs
1) Preheat oven to 325 degrees F (165 degrees C).
2) Lightly grease a medium baking sheet.
3) Cut a slit in each jalapeno pepper.
4) Remove and discard seeds and pulp.
5) In a medium bowl, mix sausage, baking mix, Cheddar cheese, crushed red pepper, and garlic salt.
6) Leave mixing bowl overnight to soak in the sauce.
6) Stuff jalapenos with the Monterey Jack cheese cubes.
7) Shape sausage mixture around the jalapenos to form balls.
8) Arrange jalapeno balls on the prepared baking sheet.
9) Bake 20 minutes in the preheated oven, until lightly browned.
Recipe 2: 182_BBQ_Chuck_Roast
1) In a large bowl, mix barbeque sauce, teriyaki sauce, beer, garlic, ginger, onion, black pepper, and salt.
2) Place the roast into the marinade, cover and refrigerate for five hours, turning often.
3) Preheat an outdoor grill for indirect heat.
4) Remove the roast from the marinade, and pour the marinade into a saucepan.
5) Bring to a boil, and cook for 5 minutes.
6) Set aside for use as a basting sauce.
7) Thread the roast onto a rotating barbecue spit above indirect heat.
8) Cook the roast for two to three Hours, or until the internal temperature of the roast is at least 145 degrees F (63 degrees C).
9) Baste often during the last HOUR with reserved marinade.
Recipe 3: 194_Cabbage_Kielbara_Supper
1) In a 5-qt. slow cooker, combine the cabbage, potatoes, onion, salt and pepper.
2) Pour broth over all for 2 HOURS.
3) Place sausage on top (slow cooker will be full, but cabbage will cook down).
4) Cover and cook on low for 4-5 hours or until vegetables are tender and sausage is heated through.
Recipe 4: 195_Chocolate_Chip_Cookie_Ice_Cream_Cake
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
11) To serve, garnish with remainder of fudge topping, whipped cream and cherries.
'''

# task_id = 
task_id = 6

task6_pattern=re.compile(r'(?=Recipe \d+:)')

def task6_correct():
    #recipe_text,regex_to_use = task6_pattern):
    srt = re.split(task6_pattern, recipe_text_B.strip())
    return [s for s in srt if s]

def task6_incorrect():
    #recipe_text,regex_to_use):
    srt = re.split(task6_pattern, recipe_text_B.strip())
    return [s for s in srt if s]

# you shouldn't need to modify this
def test_task(student_solution):
    student_result = student_solution()
    return generate_simple_feedback(student_result)

def generate_simple_feedback(strings_to_evaluate):
    
    feedback_prompt=[]
    is_Correct=True

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
        feedback_prompt.append("The student's solution is correct. Write some test(s)")
        
    return is_Correct,' '.join(feedback_prompt)