import subprocess
import json
import os

def make_path_from_relative(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

def approx_score(searchable_list, to_search):
    try:
        # Convert searchable_list to JSON string
        searchable_list_json = json.dumps(searchable_list)
        # Call the external executable with arguments
        result = subprocess.run([make_path_from_relative(r"bin/Release/net10.0/win-x64/publish/ApproxScore"), searchable_list_json, to_search], capture_output=True, text=True)
        # Check if the process ran successfully
        if result.returncode == 0:
            # Parse the JSON output
            scores = json.loads(result.stdout)
            return scores
        else:
            print("Error:", result.stderr)
            return None
    except Exception as e:
        print("Error:", e)
        return None

def print_scores(scores):
    if scores:
        print("Matching scores:")
        for score in scores:
            print(f"{score['item']}: {score['score']}")

# Example usage
if __name__ == "__main__":
    searchable_list = ["apple", "banana", "orange", "pineapple"]
    to_search = "bonnane"
    print(f'to search: {to_search}')
    scores = approx_score(searchable_list, to_search)
    print_scores(scores)
