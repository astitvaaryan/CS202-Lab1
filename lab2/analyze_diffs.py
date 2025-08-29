# lab2/analyze_diffs.py
import csv
from pydriller import Repository
from transformers import pipeline
import torch

# --- Configuration ---
REPO_URL = 'https://github.com/psf/requests' # Must be the same repo as in the first script
COMMITS_INPUT_FILE = 'commits.csv'
FILES_OUTPUT_FILE = 'files_analysis.csv'

def analyze_bug_commits():
    """
    Reads a list of bug-fix commit hashes from a CSV, analyzes the diffs
    of each modified file, gets an LLM inference, and creates a rectified message.
    """
    print("Setting up the LLM... This may take a few minutes on the first run.")
    # Setup the LLM pipeline
    device = 0 if torch.cuda.is_available() else -1
    llm = pipeline('text2text-generation', model='mamiksik/CommitPredictorT5', device=device)
    print("LLM setup complete.")

    # Read the hashes of bug-fixing commits from the first script's output
    commit_hashes = []
    with open(COMMITS_INPUT_FILE, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) # Skip the header row
        for row in csv_reader:
            commit_hashes.append(row[0]) # The hash is in the first column

    print(f"Found {len(commit_hashes)} commit hashes to analyze from {COMMITS_INPUT_FILE}.")

    # Prepare the output CSV for detailed file analysis
    with open(FILES_OUTPUT_FILE, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        # Write header row for the detailed analysis CSV
        csv_writer.writerow(["Hash", "Message", "Filename", "Source Code (before)", "Source Code (current)", "Diff", "LLM Inference (fix type)", "Rectified Message"])

        # Use pydriller to analyze ONLY the specific commits we found
        print("Analyzing diffs for each file in the bug-fix commits...")
        for commit in Repository(REPO_URL, only_commits=commit_hashes).traverse_commits():
            for modified_file in commit.modified_files:
                # We only care about Python files that were modified
                if modified_file.change_type.name == 'MODIFY' and modified_file.filename.endswith('.py'):

                    # Prepare input for the LLM using the diff
                    llm_input = f"fix: {modified_file.diff}"
                    if len(llm_input) > 1024:
                        llm_input = llm_input[:1024] # Truncate long diffs

                    # Get the LLM prediction
                    llm_result = llm(llm_input)
                    llm_inference = llm_result[0]['generated_text'] if llm_result else "LLM failed"

                    # Your Rectifier logic goes here
                    rectified_message = f"[{modified_file.new_path}] {llm_inference}"

                    # Write the detailed analysis for the file to the CSV
                    csv_writer.writerow([
                        commit.hash,
                        commit.msg,
                        modified_file.new_path,
                        modified_file.source_code_before,
                        modified_file.source_code,
                        modified_file.diff,
                        llm_inference,
                        rectified_message
                    ])

    print(f"\nFinished analysis. Detailed data saved to {FILES_OUTPUT_FILE}")

if __name__ == "__main__":
    analyze_bug_commits()