from prompt_generator import generate_prompts_kfolds, generate_sample, generate_prompts_inference
from metadata import *
from apikeys import *

import pickle
import json
import requests
import time

for i in range(num_test):
    sample = generate_sample(i, num_pts)
    prompts = generate_prompts_kfolds(num_folds, sample, i)
    responses = []
    for n in range(num_folds):
        wrapper = prompts[n][0]
        response_n = []
        for w in range(1, len(wrapper)):
            while True:
                try:
                    response = requests.post(
                        url="https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": OpenRouterKey,
                        },
                        data=json.dumps({
                            "model": "anthropic/claude-3.5-sonnet-20240620",
                            "messages": [{"role": "user", "content": wrapper[0]}, {"role": "user", "content": wrapper[w]}],
                            "temperature": 0
                        })
                    )
                    print(response.text)
                    print(response.json()['choices'][0]['message'])
                    response_n.append(response.json()['choices'][0]['message'])
                    break
                except Exception as e:
                    print(e)
                    time.sleep(1)
        responses.append(response_n)
    with open(f"claude_index_{i}_responses_kfolds.pkl", "wb") as f:
        pickle.dump(responses, f)
    prompt_strings = [prompt[0] for prompt in prompts]
    with open(f"claude_index_{i}_prompts_kfolds.pkl", "wb") as f:
        pickle.dump(prompt_strings, f)
    targets = [prompt[1] for prompt in prompts]
    with open(f"claude_index_{i}_targets_kfolds.pkl", "wb") as f:
        pickle.dump(targets, f)

    prompt, target = generate_prompts_inference(sample, i)
    responses = []
    for w in range(1, len(prompt)):
        while True:
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": OpenRouterKey,
                    },
                    data=json.dumps({
                        "model": "anthropic/claude-3.5-sonnet-20240620",  # Optional
                         "messages": [{"role": "user", "content": prompt[0]}, {"role": "user", "content": prompt[w]}],
                        "temperature": 0
                    })
                )
                print(response.text)
                print(response.json()['choices'][0]['message'])
                responses.append(response.json()['choices'][0]['message'])
                break
            except Exception as e:
                print(e)
                time.sleep(1)
    with open(f"claude_index_{i}_responses_inference.pkl", "wb") as f:
        pickle.dump(responses, f)
    with open(f"claude_index_{i}_prompts_inference.pkl", "wb") as f:
        pickle.dump(prompt, f)
    with open(f"claude_index_{i}_targets_inference.pkl", "wb") as f:
        pickle.dump(target, f)
