from metadata import *
import pickle
import numpy as np

def interval_calculator(llm):
    successes_kfolds = 0
    successes_inference = 0
    intervals_kfolds = []
    intervals_inference = []
    for i in range(num_test):
        distribution = []
        neg_distribution = []
        with open(f"{llm}_index_{i}_responses_kfolds.pkl", "rb") as f:
            responses_kfolds = pickle.load(f)
        with open(f"{llm}_index_{i}_targets_kfolds.pkl", "rb") as f:
            targets_kfolds = pickle.load(f)
        for k in range(num_folds):
            residuals = []
            targets = targets_kfolds[k].split(",")
            responses = [response['content'] for response in responses_kfolds[k]]
            for j in range(len(targets) - 1):
                residuals.append(abs(int(targets[j]) - int(responses[j])))
            for residual in residuals:
                distribution.append(residual + int(responses[-1]))
                neg_distribution.append(residual - int(responses[-1]))
        target_test = int(targets_kfolds[0][-3:])
        quantile_level_kfold = (1 - alpha) * (1 + (1 / num_pts))
        lower_quantile = -1 * np.quantile(neg_distribution, quantile_level_kfold)
        upper_quantile = np.quantile(distribution, quantile_level_kfold)
        if lower_quantile <= target_test <= upper_quantile:
            successes_kfolds += 1
        intervals_kfolds.append((lower_quantile, upper_quantile))

        with open(f"{llm}_index_{i}_responses_inference.pkl", "rb") as f:
            responses_inference = pickle.load(f)
        with open(f"{llm}_index_{i}_targets_inference.pkl", "rb") as f:
            targets_inference = pickle.load(f)
        residuals = []
        targets = targets_inference.split(",")
        responses = [response['content'] for response in responses_inference]
        for j in range(len(targets) - 1):
            residuals.append(abs(int(targets[j]) - int(responses[j])))
        quantile_level_inference = (1 - alpha) * (1 + (1 / (num_pts / 2)))
        q_hat = np.quantile(residuals, quantile_level_inference)
        lower_quantile = min(int(responses[-1]) - q_hat, int(responses[-1]) + q_hat)
        upper_quantile = max(int(responses[-1]) - q_hat, int(responses[-1]) + q_hat)
        if lower_quantile <= int(targets[-1]) <= upper_quantile:
            successes_inference += 1
        intervals_inference.append((lower_quantile, upper_quantile))
    return successes_kfolds / num_test, successes_inference / num_test, intervals_kfolds, intervals_inference









