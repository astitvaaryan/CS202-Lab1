import csv
from pydriller import Repository

# 1. Define your criteria and repository
repo_url = 'https://github.com/psf/requests'
# bug_keywords = ['fix', 'bug', 'error', 'patch', 'resolve', 'correct']
bug_keywords = [
    "fixed", "bug", "fixes", "fix", "patch", "correct" "crash", "solves", "resolves", "issue",
    "regression", "fall back", "assertion", "coverity", "reproducible",
    "stack-wanted", "steps-wanted", "testcase", "failur", "fail", "npe",
    "except", "broken", "differential testing", "error", "hang", "test fix",
    "steps to reproduce", "failure", "leak", "stack trace", "heap overflow",
    "freez", "problem", "overflow", "avoid", "workaround", "break", "stop"
]

# 2. Prepare the CSV file to store commit info
# This matches the table in the lab description [cite: 101]
csv_commits_file = open('commits.csv', 'w', newline='', encoding='utf-8')
csv_commits_writer = csv.writer(csv_commits_file)
csv_commits_writer.writerow(["Hash", "Message", "Hashes of parents", "Is a merge commit?", "List of modified files"])

print(f"Mining repository: {repo_url}")

# 3. Traverse the repository for bug-fixing commits
for commit in Repository(repo_url).traverse_commits():
    # Our strategy: check if the commit message contains any bug-related keywords
    is_bug_fix = any(keyword in commit.msg.lower() for keyword in bug_keywords)

    if is_bug_fix:
        # Extract parent hashes
        parent_hashes = ', '.join([p for p in commit.parents])

        # Extract modified file paths
        modified_files_list = [file.new_path or file.old_path for file in commit.modified_files]
        modified_files_str = ', '.join(filter(None, modified_files_list))

        # Write the collected data to the CSV
        csv_commits_writer.writerow([
            commit.hash,
            commit.msg,
            parent_hashes,
            commit.merge,
            modified_files_str
        ])

# 4. Close the file
csv_commits_file.close()
print("Finished mining commits. Data saved to commits.csv")