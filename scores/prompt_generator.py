import json
import random

list_of_attributes = '''
1: total income in the last 12 months
2: total savings in the last 12 months
3: total existing debt
4: ratio of savings to income
5: ratio of debt to income
6: ratio of debt to savings
7: expenditure on clothing in the past 12 months
8: expenditure on clothing in the past 6 months
9: expenditure on education in the past 12 months
10: expenditure on education in the past 6 months
11: expenditure on entertainment in the past 12 months
12: expenditure on entertainment in the past 6 months
14: expenditure on fines in the past 6 months
15: expenditure on gambling in the past 12 months
16: expenditure on gambling in the past 6 months
17: expenditure on groceries in the past 12 months
18: expenditure on groceries in the past 6 months
19: expenditure on health in the past 12 months
20: expenditure on health in the past 6 months
21: expenditure on housing in the past 12 months
22: expenditure on housing in the past 6 months
23: expenditure on tax in the past 12 months
24: expenditure on tax in the past 6 months
25: expenditure on travel in the past 12 months
26: expenditure on travel in the past 6 months
27: expenditure on utilities in the past 12 months
28: expenditure on utilities in the past 6 months
29: expenditure on expenditure in the past 12 months
30: expenditure on expenditure in the past 6 months
31: gambling habit (none, low, high)
32: whether or not individual possesses debt (0 = no, 1 = yes)
33: whether or not individual possesses mortgage (0 = no, 1 = yes)
34: whether or not individual possesses dependents (0 = no, 1 = yes)
'''

def generate_prompts_kfolds(num_folds, sample, index_test):
    with open("credit_scores.json", "r") as f:
        scores = json.load(f)
    sample_strings = [scores[str(x)] for x in sample]
    folds = []
    fold_size = len(sample) // num_folds
    for i in range(num_folds):
        folds.append(sample_strings[(i * fold_size):((i + 1) * fold_size)])
    prompts = []
    for fold in folds:
        prompt_wrapper = []
        prompt = "Here is a list of attributes listed in order. \n"
        prompt += list_of_attributes
        prompt += ("\nNow, you will receive a sequence of individuals with values corresponding to each of the attributes above, "
                   "as well as their credit scores. Use this information to guide you in your predictions.")
        target = ""
        for other_fold in folds:
            if other_fold != fold:
                for string in other_fold:
                    prompt += string + "\n"
        prompt_wrapper.append(prompt)
        for string in fold:
            query = ("Now, given this individual with values corresponding to each of the attributes above, predict their credit score. "
                     "Your output should be only a 3 digit number, such as xyz, and nothing else.")
            lines = string.splitlines()
            temp_lines = lines[:-1]
            temp_string = "\n".join(temp_lines)
            query += temp_string + "\n"
            target += lines[-1][-3:] + ","
            prompt_wrapper.append(query)
        query = ("Now, given this individual with values corresponding to each of the attributes above, predict their credit score. "
            "Your output should be only a 3 digit number, such as xyz, and nothing else.")
        lines_target = scores[str(index_test)].splitlines()
        temp_lines = lines_target[:-1]
        temp_string = "\n".join(temp_lines)
        query += temp_string + "\n"
        target += lines_target[-1][-3:]
        prompt_wrapper.append(query)
        prompts.append((prompt_wrapper, target))
    return prompts

def generate_prompts_inference(sample, index_test):
    with open("credit_scores.json", "r") as f:
        scores = json.load(f)
    sample_strings = [scores[str(x)] for x in sample]
    folds = []
    fold_size = len(sample) // 2
    for i in range(2):
        folds.append(sample_strings[(i * fold_size):((i + 1) * fold_size)])
    prompt_wrapper = []
    prompt = "Here is a list of attributes listed in order. \n"
    prompt += list_of_attributes
    prompt += ("\nNow, you will receive a sequence of individuals with values corresponding to each of the attributes above, "
               "as well as their credit scores. Use this information to guide you in your predictions.")
    target = ""
    fold = folds[0]
    other_fold = folds[1]
    for string in other_fold:
        prompt += string + "\n"
    prompt_wrapper.append(prompt)
    for string in fold:
        query = ("Now, given this individual with values corresponding to each of the attributes above, predict their credit score. "
            "Your output should be only a 3 digit number, such as xyz, and nothing else.")
        lines = string.splitlines()
        temp_lines = lines[:-1]
        temp_string = "\n".join(temp_lines)
        query += temp_string + "\n"
        target += lines[-1][-3:] + "\n"
        prompt_wrapper.append(query)
    query = ("Now, given this individual with values corresponding to each of the attributes above, predict their credit score. "
        "Your output should be only a 3 digit number, such as xyz, and nothing else.")
    lines_target = scores[str(index_test)].splitlines()
    temp_lines = lines_target[:-1]
    temp_string = "\n".join(temp_lines)
    query += temp_string + f"\n"
    target += lines_target[-1][-3:] + "\n"
    prompt_wrapper.append(query)
    return prompt_wrapper, target

def generate_prompt_test(index_test):
    with open("credit_scores.json", "r") as f:
        scores = json.load(f)
    prompt = "Here is a list of attributes listed in order. \n"
    prompt += list_of_attributes
    prompt += "Now, you will receive an individual with values corresponding to each of the attributes above."
    prompt += scores[str(index_test)]
    prompt += "\nList out this individual's attributes one by one and their corresponding values."
    return prompt

def generate_sample(index_test, num_pts):
    sample = random.sample(range(1000), num_pts)
    while index_test in sample:
        sample = random.sample(range(1000), num_pts)
    return sample



