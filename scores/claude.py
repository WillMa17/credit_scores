from prompt_generator import generate_prompts, generate_sample

import anthropic

# client = anthropic.Anthropic(api_key='null')
# response = client.messages.create(
#     model="claude-3-5-sonnet-20240620",
#     max_tokens=1024,
#     messages=[{"role": "user", "content": "blah"}]
# )

sample = generate_sample(1, 10)
print(generate_prompts(5, sample)[0][0])
print(generate_prompts(5, sample)[0][1])