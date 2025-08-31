# lab2/evaluate.py (Updated Version)
import pandas as pd
import matplotlib.pyplot as plt
import os
import re # Using re for more robust splitting

# --- Configuration ---
ANALYSIS_FILE = 'files_analysis.csv'

def is_precise(message, filename):
    """
    A more flexible rule for a "precise" commit message.
    It checks if ANY significant part of the file path is in the message.
    e.g., for 'requests/adapters.py', it checks for 'requests' OR 'adapters'.
    """
    if not isinstance(message, str) or not filename:
        return False
    
    try:
        # Split the full path by slashes, backslashes, dots, and underscores
        parts = re.split(r'[\\/._]', filename)
        
        # Create a set of unique, meaningful keywords from the path parts
        keywords = {p.lower() for p in parts if len(p) > 3 and p.lower() not in ['py', 'lib', 'src', 'tests']}
        
        if not keywords:
            return False
        
        # Return True if any of the keywords are found in the message
        return any(keyword in message.lower() for keyword in keywords)
    except:
        return False

# The rest of the script (the evaluate_results function) remains exactly the same.
def evaluate_results():
    """
    Loads the analysis data and calculates the hit rates for the three RQs.
    """
    print(f"Loading data from {ANALYSIS_FILE}...")
    try:
        df = pd.read_csv(ANALYSIS_FILE)
    except FileNotFoundError:
        print(f"Error: {ANALYSIS_FILE} not found. Please run the analysis script first.")
        return

    required_columns = ["Message", "LLM Inference (fix type)", "Rectified Message", "Filename"]
    if not all(col in df.columns for col in required_columns):
        print(f"Error: CSV file is missing one of the required columns: {required_columns}")
        return
            
    df['dev_precise'] = df.apply(lambda row: is_precise(row['Message'], row['Filename']), axis=1)
    dev_hit_rate = (df['dev_precise'].sum() / len(df)) * 100

    df['llm_precise'] = df.apply(lambda row: is_precise(row['LLM Inference (fix type)'], row['Filename']), axis=1)
    llm_hit_rate = (df['llm_precise'].sum() / len(df)) * 100

    df['rectifier_precise'] = df.apply(lambda row: is_precise(row['Rectified Message'], row['Filename']), axis=1)
    rectifier_hit_rate = (df['rectifier_precise'].sum() / len(df)) * 100
    
    print("\n--- Evaluation Results (with updated precision logic) ---")
    print(f"{'Metric':<25} | {'Hit Rate (%)':<15}")
    print("-" * 45)
    print(f"{'RQ1: Developer Precision':<25} | {dev_hit_rate:<15.2f}")
    print(f"{'RQ2: LLM Precision':<25} | {llm_hit_rate:<15.2f}")
    print(f"{'RQ3: Rectifier Precision':<25} | {rectifier_hit_rate:<15.2f}")
    print("-" * 45)

    labels = ['Developer', 'LLM', 'Rectifier']
    rates = [dev_hit_rate, llm_hit_rate, rectifier_hit_rate]

    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, rates, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.ylabel('Hit Rate (%)')
    plt.title('Precision Hit Rate Comparison (Flexible Definition)')
    plt.ylim(0, 100)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f}%', va='bottom', ha='center')

    plot_filename = 'evaluation_results_flexible.png'
    plt.savefig(plot_filename)
    print(f"\nChart saved to {plot_filename}")

if __name__ == "__main__":
    evaluate_results()