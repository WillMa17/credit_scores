from prompt_generator import generate_sample
from metadata import *
import pickle

for i in range(num_test):
    sample = generate_sample(i, num_pts)
    with open(f"index_{i}_sample.pkl", "wb") as f:
        pickle.dump(sample, f)

