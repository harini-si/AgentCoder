import argparse
import os
import json
from tqdm import tqdm
import copy
from openai import OpenAI

client = OpenAI()
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time
from datasets import load_dataset


# load dataset from json
with open("../prompts/factorsim_prompts.json", "r") as f:
    dataset = json.load(f)



prompt_path = "../prompts/factorsim_programmer_prompt.txt"
with open(prompt_path, "r") as f:
    construct_few_shot_prompt = f.read()


def preprocess_data(completion_string):
    if f"```python" in completion_string:
        completion_string = completion_string[
            completion_string.find(f"```python") + len(f"```python") :
        ]
        completion_string = completion_string[: completion_string.find("```")]
    else:
        print("Error: No code block found")
    return completion_string


def call_fetch_completion_helper(dataset, model, lg):
    print("Fixing bug...")
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_entry = {
            executor.submit(fetch_completion, copy.deepcopy(entry), model, lg): entry
            for entry in tqdm(dataset)
        }
        for future in tqdm(concurrent.futures.as_completed(future_to_entry)):
            entry = future_to_entry[future]
            try:
                updated_entry = future.result()
                idx = dataset.index(entry)
                dataset[idx] = updated_entry
            except Exception as e:
                print(repr(e))
    return dataset
# Function to fetch completion
def fetch_completion(data_entry, model, lg, times=10):
    global construct_few_shot_prompt
    prompt = data_entry["prompt"]
    existing_code= data_entry["backbone"]
    text = f"""
{construct_few_shot_prompt}

{prompt}
Follow the specifications provided in the subsequent (incomplete) implementation closely: it's essential to retain all variables defined in the format shown, as our unit testing code will interact with the variables established in this incomplete implementation.

**Input Code Snippet**:
```python
{existing_code}
```
- Do not hallucinate external image files (e.g., .png, .jpg) or sound effects(e.g., mp3).
- PLEASE RETURN THE COMPLETE IMPLEMENTATION OF THE GAME, NOT JUST THE PROVIDED EXISTING CODE.
"""
    completions_code = []
    for i in range(times):
        while True:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": text},
                    ],
                )
                completion = response.choices[0].message.content
                completion = preprocess_data(completion)

            except Exception as e:
                print(e)
                time.sleep(10)
                completion = ""
            if completion != "":
                break
        completions_code.append(completion)

    data_entry["completion_list"] = completions_code
    return data_entry


if __name__ == "__main__":
    model_list = ["gpt-3.5-turbo-1106"]
    language = ["python"]
    for model in model_list:
        for lg in language:

            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_entry = {
                    executor.submit(
                        fetch_completion, copy.deepcopy(entry), model, lg
                    ): entry
                    for entry in tqdm(dataset)
                }
                for future in tqdm(concurrent.futures.as_completed(future_to_entry)):
                    entry = future_to_entry[future]
                    try:
                        updated_entry = future.result()
                        idx = dataset.index(entry)
                        dataset[idx] = updated_entry
                    except Exception as e:
                        print(repr(e))
            with open(
                f"../dataset/{model}_{lg}.json", "w"
            ) as f:
                json.dump(dataset, f, indent=4)
