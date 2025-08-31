import pandas as pd
from tqdm import tqdm
# --- UPDATED IMPORTS for the new radon API ---
from radon.visitors import ComplexityVisitor
from radon.metrics import mi_visit
from radon.raw import analyze

LAB2_DATA_FILE = 'files_analysis.csv'
INTERMEDIATE_OUTPUT_FILE = 'lab3_with_radon.csv'

# --- UPDATED FUNCTION to use the new radon API ---
def get_radon_metrics(source_code):
    """Calculates radon metrics (MI, CC, LOC) for a source code string."""
    if not isinstance(source_code, str) or not source_code.strip():
        return 0.0, 0, 0
    try:
        # 1. Cyclomatic Complexity
        visitor = ComplexityVisitor.from_code(source_code)
        total_cc = sum(func.complexity for func in visitor.functions)

        # 2. Maintainability Index
        mi_score = mi_visit(source_code, multi=True)

        # 3. Lines of Code
        raw_analysis = analyze(source_code)
        loc = raw_analysis.loc
        
        return mi_score, total_cc, loc
    except Exception:
        # This can happen if the source code has a syntax error
        return 0.0, 0, 0

def calculate_structural_metrics():
    df = pd.read_csv(LAB2_DATA_FILE).dropna(subset=['Source Code (before)', 'Source Code (current)'])
    print("Starting structural metric analysis with Radon...")

    # (c) Structural Metrics with radon
    tqdm.pandas(desc="Radon (Before)");
    df[['MI_Before', 'CC_Before', 'LOC_Before']] = df['Source Code (before)'].progress_apply(lambda x: pd.Series(get_radon_metrics(x))) #
    
    tqdm.pandas(desc="Radon (After)");
    df[['MI_After', 'CC_After', 'LOC_After']] = df['Source Code (current)'].progress_apply(lambda x: pd.Series(get_radon_metrics(x))) #
    
    df['MI_Change'] = df['MI_After'] - df['MI_Before'] #
    df['CC_Change'] = df['CC_After'] - df['CC_Before'] #
    df['LOC_Change'] = df['LOC_After'] - df['LOC_Before'] #

    df.to_csv(INTERMEDIATE_OUTPUT_FILE, index=False)
    print(f"\nRadon analysis complete. Intermediate data saved to {INTERMEDIATE_OUTPUT_FILE}")

if __name__ == "__main__":
    calculate_structural_metrics()