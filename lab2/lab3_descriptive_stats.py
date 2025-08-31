import pandas as pd

# The starting point is your Lab 2 dataset [cite: 23]
LAB2_DATA_FILE = 'files_analysis.csv'

def run_descriptive_analysis():
    """
    Loads the Lab 2 dataset and computes baseline descriptive statistics as per Activity (b).
    """
    print(f"Loading data from {LAB2_DATA_FILE}...")
    try:
        df = pd.read_csv(LAB2_DATA_FILE)
    except FileNotFoundError:
        print(f"Error: {LAB2_DATA_FILE} not found. Please ensure it is in the project root directory.")
        return

    print("\n--- Baseline Descriptive Statistics ---")
    
    # Calculate the total number of unique commits and files [cite: 28]
    total_commits = df['Hash'].nunique()
    total_files = len(df)
    print(f"Total unique bug-fix commits: {total_commits}")
    print(f"Total modified file entries: {total_files}")
    
    # Calculate the average number of modified files per commit [cite: 29]
    if total_commits > 0:
        avg_files = df.groupby('Hash')['Filename'].nunique().mean()
        print(f"Average modified files per commit: {avg_files:.2f}")
    
    # Show the distribution of fix types [cite: 30]
    print("\nDistribution of fix types (from LLM):")
    print(df['LLM Inference (fix type)'].value_counts().head())
    
    # Find the most frequently modified file extensions [cite: 31]
    # Create an 'extension' column for analysis
    df['extension'] = df['Filename'].str.split('.').str[-1]
    print("\nMost frequently modified file extensions:")
    print(df['extension'].value_counts().head())

if __name__ == "__main__":
    run_descriptive_analysis()