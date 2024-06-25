import os
import re
import json
from openai import OpenAI
import json
import re
import os
import subprocess
import signal
import sys
import tempfile
import importlib.util
from programmer_factorsim import call_fetch_completion_helper


import sys

os.environ["SDL_VIDEODRIVER"] = "dummy"
def run_code(code, timeout=10):
    # Timeout handler function
    def timeout_handler(signum, frame):
        raise TimeoutError

    try:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)

        code = "import os\n" + 'os.environ["SDL_VIDEODRIVER"] = "dummy"\n' + code
        # Create a temporary Python file to store the code
        with tempfile.NamedTemporaryFile(
            suffix=".py", delete=False, mode="w"
        ) as tmp_file:
            tmp_file_name = tmp_file.name
            tmp_file.write(code)

        # Run the Python script using subprocess
        result = subprocess.run(
            ["python", tmp_file_name], capture_output=True, text=True
        )

        # Capture stdout and stderr
        stdout = result.stdout
        stderr = result.stderr

        signal.alarm(0)
        return stdout, stderr

    except TimeoutError:
        return None, "The code took too long to execute."

def save_json_to_file(json_data, file_path):
    # even if the file_path is not valid, it will create the file
    with open(file_path, "w+") as f:
        json.dump(json_data, f, indent=4)

# Timeout handler function
def timeout_handler(signum, frame):
    raise TimeoutError
def run_sanity_check(code):
    try:
        no_condition_code = code.replace("while running:", "for _ in range(300):")
        stdout, stderr = run_code(no_condition_code)
        return stdout, stderr
    except:
        stdout = ""
        stderr = "code failed to run"
        return stdout, stderr

def execute_file(test_file_path, implementation_path):
    result = subprocess.run(
        ["python", test_file_path, implementation_path], capture_output=True, text=True
    )

    stdout = result.stdout
    stderr = result.stderr
    # print(stdout)
    # print(stderr)
    # Use regular expressions to find passed tests
    passed_tests = re.findall(r"test_[a-zA-Z_0-9]+ \(.*\) ... ok", stderr)
    passed_tests = [
        re.match(r"(test_[a-zA-Z_0-9]+) \(.*\) ... ok", test).group(1)
        for test in passed_tests
    ]

    # Use regular expressions to find failed tests
    failed_tests = re.findall(r"test_[a-zA-Z_0-9]+ \(.*\) ... FAIL", stderr)
    failed_tests = [
        re.match(r"(test_[a-zA-Z_0-9]+) \(.*\) ... FAIL", test).group(1)
        for test in failed_tests
    ]

    error_tests = re.findall(r"test_[a-zA-Z_0-9]+ \(.*\) ... ERROR", stderr)
    error_tests = [
        re.match(r"(test_[a-zA-Z_0-9]+) \(.*\) ... ERROR", test).group(1)
        for test in error_tests
    ]
    return passed_tests, failed_tests, error_tests

def run_eval(test_file_path, implementation_path, game_name, timeout=20):
    json_result = None
    try:
        # Set the signal alarm
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        passed_tests, failed_tests, error_tests = execute_file(
            test_file_path, implementation_path
        )
        # with open(f"{game_name}_test_results.json", "r") as f:
        #     json_result = json.load(f)
        total_tests = len(passed_tests) + len(failed_tests) + len(error_tests)
        # print(f"GPT4 (context) Passed Tests for {game_name}: {passed_tests}")
        # print(f"GPT4 (context) Failed Tests for {game_name}: {failed_tests}")
        # print(f"GPT4 (context) Error Tests for {game_name}: {error_tests}\n")
        if total_tests == 0:
            # couldn't eveen import the file
            acc = 0
        else:
            acc = len(passed_tests) / total_tests
        signal.alarm(0)

    except TimeoutError:
        print("function timed out")
        acc = 0
    json_result = ""
    return json_result, acc


if __name__ == "__main__":
    model = "gpt-3.5-turbo-1106"
    lg = "python"
    with open(f'../dataset/{model}_{lg}.json') as f:
        dataset = json.load(f)
        
    for i in range(2):
        for game in dataset:
            game_name = game["game"]
            completion_list = game["completion_list"]
            tests = game["test_case_list"]
            
            for idx in range(len(completion_list)):
                print(f"Running {game_name} {idx}")
                completion = completion_list[idx]
                tests= tests[idx]
                test_file_path = f"../temp_test.py"
                implementation_path = f"../temp_implementation.py"
                with open(test_file_path, "w") as f:
                    f.write(tests)
                with open(implementation_path, "w") as f:
                    f.write(completion)
                
                json_result, acc = run_eval(test_file_path, implementation_path, game_name=game_name)
                dataset[idx]["report_result"] = json_result
                dataset[idx]["report_accuracy"] = acc
                dataset[idx]['passed'] = acc == 1.0
        dataset = call_fetch_completion_helper(dataset, model, lg)
        with open(f'../dataset/{model}_{lg}.json', 'w') as f:
            json.dump(dataset, f, indent=4)
        
