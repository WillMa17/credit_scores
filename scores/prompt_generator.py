import json
import random

def generate_prompts(num_folds, sample):
    with open("credit_scores.json", "r") as f:
        scores = json.load(f)
    sample_strings = [scores[str(x)] for x in sample]
    folds = []
    fold_size = len(sample) // num_folds
    for i in range(num_folds):
        folds.append(sample_strings[(i * fold_size):((i + 1) * fold_size)])
    prompts = []
    for fold in folds:
        prompt = ("This is a sequence of individuals with attributes and their credit score. "
                        "Use this information as a guiding tool to predict individuals' credit scores.\n")
        prompt_target = ""
        for other_fold in folds:
            if other_fold != fold:
                for string in other_fold:
                    prompt += string + "\n"
        prompt += ("Now, you will receive a sequence of individuals with attributes. "
                   "Respond by predicting each of their credit scores, and nothing else.\n")
        for string in fold:
            lines = string.splitlines()
            temp_lines = lines[:-1]
            temp_string = "\n".join(temp_lines)
            prompt += temp_string + "\nPredict this individual's credit score.\n"
            prompt_target += lines[-1] + "\n"
        prompts.append((prompt, prompt_target))
    return prompts

def generate_sample(index_test, num_pts):
    sample = random.sample(range(1000), num_pts)
    while index_test in sample:
        sample = random.sample(range(1000), num_pts)
    return sample



