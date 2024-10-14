from metadata import *
import pickle

def interval_calculator(llm):
    for i in range(num_test):
        distribution = []
        with open(f"{llm}_index_{i}_responses_kfolds.pkl", "rb") as f:
            responses_kfolds = pickle.load(f)
        with open(f"{llm}_index_{i}_targets_kfolds.pkl", "rb") as f:
            targets_kfolds = pickle.load(f)
        for k in range(num_folds):

