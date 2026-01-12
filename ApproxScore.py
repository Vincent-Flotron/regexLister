import subprocess
import json
from Tools import Tools
import os

class ApproxScore:
    @staticmethod
    def approx_score(searchable_list, to_search):
        """Function to calculate match score between two strings"""
        try:
            # Convert searchable_list to JSON string
            searchable_list_json = json.dumps(searchable_list)
            # Call the external executable with arguments
            rel_path_to_approx_search = ApproxScore.get_rel_path_to_approx_search()
            full_path_to_approx_search = Tools.make_path_from_relative(rel_path_to_approx_search)
            ApproxScore.compile_approx_search_if_not(full_path_to_approx_search)
            result = subprocess.run([full_path_to_approx_search, searchable_list_json, to_search], capture_output=True, text=True)
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

    @staticmethod
    def compile_approx_search_if_not(full_path_to_approx_search):
        if not os.path.exists(full_path_to_approx_search):
            path = Tools.make_path_from_relative('ApproxScore')
            os.chdir(path)
            ApproxScore.compile(f"{path}/compile.bat")
        if not os.path.exists(full_path_to_approx_search):
            raise Exception(f"File '{full_path_to_approx_search}' doesn't exist and couldn't be compiled.")

    @staticmethod
    def get_rel_path_to_approx_search():
        if Tools.is_windows():
            return r'ApproxScore/bin/Release/net10.0/win-x64/publish/ApproxScore.exe'
        if Tools.is_linux():
            return r'ApproxScore/bin/Release/net10.0/win-x64/publish/ApproxScore'


    @staticmethod
    def print_scores(scores):
        if scores:
            print("Matching scores:")
            for score in scores:
                print(f"{score['item']}: {score['score']}")

    @staticmethod
    def compile(compile_bat_file_path):
        # Check if the file exists
        if not os.path.isfile(compile_bat_file_path):
            raise FileNotFoundError(f"The batch file does not exist: {compile_bat_file_path}")

        # Run the batch file
        result = subprocess.run(
            [compile_bat_file_path],
            capture_output=True,
            text=True,
            shell=True  # Required for .bat files on Windows
        )

        # Check for errors
        if result.returncode != 0:
            print("Error:", result.stderr)
            return False

        print("Output:", result.stdout)
        return True

# Example usage
if __name__ == "__main__":
    searchable_list = ["apple", "banana", "orange", "pineapple"]
    to_search = "bonnane"
    print(f'to search: {to_search}')
    scores = ApproxScore.approx_score(searchable_list, to_search)
    ApproxScore.print_scores(scores)
