import argparse
import os
import json
from tqdm import tqdm
import copy
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time
client = OpenAI()
from datasets import load_dataset

# load dataset from json
with open("../prompts/factorsim_prompts.json", "r") as f:
    dataset = json.load(f)

dataset = dataset[0:1]

prompt_path = "../prompts/test_designer_factorsim_prompt.txt"
with open(prompt_path, "r") as f:
    construct_few_shot_prompt = f.read()


def preprocess_data(test_case_string):
    if f"```python" in test_case_string:
        test_case_string = test_case_string[
            test_case_string.find(f"```python") + len(f"```python") :
        ]
        test_case_string = test_case_string[: test_case_string.find("```")]

    return test_case_string


# Function to fetch completion
def fetch_completion(data_entry, model, lg, times=1):
    global construct_few_shot_prompt

    prompt = data_entry["prompt"]
    existing_code = data_entry["backbone"]
   

    text = f"""
{construct_few_shot_prompt}

{prompt}
**Input Code Snippet**:
```python
{existing_code}
```

"""
    test_case_list = []
    for i in range(times):
        while True:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a code developer assistant."},
                        {"role": "user", "content": text},
                    ],
                )
                test = response.choices[0].message.content
                test_case = preprocess_data(test)
                
            except Exception as e:
                time.sleep(20)
                print(e)
                test_case = ""
            if test_case != "":
                break
        test_case_list.append(test_case)
    data_entry["test_case_list"] = test_case_list
    return data_entry





if __name__ == "__main__":
    model_list = ["gpt-3.5-turbo-1106"]
    language = ["python"]
    for model in model_list:
        for lg in language:
            from datasets import load_dataset

            with open(f"../dataset/{model}_{lg}.json", "r") as f:
                dataset = json.load(f)
  
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

            with open(f"../dataset/{model}_{lg}.json", "w") as f:
                json.dump(dataset, f, indent=4)
