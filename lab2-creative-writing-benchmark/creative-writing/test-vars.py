import pandas as pd

def generate_tests():
    num_tests = 20

    f_action=open('data/action.txt')
    f_attribute=open('data/attribute.txt')
    f_character=open('data/character.txt')
    f_core_concept=open('data/core_concept.txt')
    f_method=open('data/method.txt')
    f_motivation=open('data/motivation.txt')
    f_object=open('data/object.txt')
    f_setting=open('data/setting.txt')
    f_timeframe=open('data/timeframe.txt')
    f_tone=open('data/tone.txt')

    lines_action=f_action.readlines()
    lines_attribute=f_attribute.readlines()
    lines_character=f_character.readlines()
    lines_core_concept=f_core_concept.readlines()
    lines_method=f_method.readlines()
    lines_motivation=f_motivation.readlines()
    lines_object=f_object.readlines()
    lines_setting=f_setting.readlines()
    lines_timeframe=f_timeframe.readlines()
    lines_tone=f_tone.readlines()

    test_cases = []
    for line in range(num_tests):
        test_case = {
            "vars": {
                "action": lines_action[line],
                "attribute": lines_attribute[line],
                "character": lines_character[line],
                "core_concept": lines_core_concept[line],
                "method": lines_method[line],
                "motivation": lines_motivation[line],
                "object": lines_object[line],
                "setting": lines_setting[line],
                "timeframe": lines_timeframe[line],
                "tone": lines_tone[line]
            }
        }
        test_cases.append(test_case)
    return test_cases

# if __name__ == "__main__":
    # tests = generate_tests()
    # print(tests)