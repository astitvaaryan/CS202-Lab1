import pandas as pd
import numpy as np
from transformers import RobertaTokenizer, RobertaModel
import torch
import sacrebleu
from tqdm import tqdm

INTERMEDIATE_DATA_FILE = 'lab3_with_radon.csv'
FINAL_OUTPUT_FILE = 'lab3_final_analysis.csv'

# (Helper functions: get_semantic_similarity, get_token_similarity - from previous answers)
def get_semantic_similarity(code1, code2, model, tokenizer, device):
    try:
        inputs1 = tokenizer(code1, return_tensors="pt", truncation=True, max_length=512, padding=True).to(device)
        inputs2 = tokenizer(code2, return_tensors="pt", truncation=True, max_length=512, padding=True).to(device)
        with torch.no_grad():
            emb1 = model(**inputs1).pooler_output; emb2 = model(**inputs2).pooler_output
        return torch.nn.functional.cosine_similarity(emb1, emb2).item()
    except Exception: return 0.0

def get_token_similarity(code1, code2):
    try: return sacrebleu.corpus_bleu([code2], [[code1]]).score / 100.0
    except Exception: return 0.0

def calculate_magnitude_and_classify():
    df = pd.read_csv(INTERMEDIATE_DATA_FILE)
    print("Starting similarity and classification analysis...")

    # (d) Change Magnitude Metrics
    print("\nSetting up CodeBERT model..."); device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base") #
    model = RobertaModel.from_pretrained("microsoft/codebert-base").to(device) #
    print(f"CodeBERT is running on: {device}")
    
    print("Calculating similarities..."); tqdm.pandas(desc="Semantic Similarity (CodeBERT)")
    df['Semantic_Similarity'] = df.progress_apply(lambda row: get_semantic_similarity(row['Source Code (before)'], row['Source Code (current)'], model, tokenizer, device), axis=1) #
    tqdm.pandas(desc="Token Similarity (BLEU)"); df['Token_Similarity'] = df.progress_apply(lambda row: get_token_similarity(row['Source Code (before)'], row['Source Code (current)']), axis=1) #

    # (e) Classification & Agreement
    print("\nClassifying fixes..."); df['Semantic_Class'] = np.where(df['Semantic_Similarity'] < 0.80, 'Major', 'Minor') #
    df['Token_Class'] = np.where(df['Token_Similarity'] < 0.75, 'Major', 'Minor') #
    df['Classes_Agree'] = np.where(df['Semantic_Class'] == df['Token_Class'], 'YES', 'NO') #
    
    df.to_csv(FINAL_OUTPUT_FILE, index=False)
    print(f"\nAnalysis complete! Final data saved to {FINAL_OUTPUT_FILE}")

if __name__ == "__main__":
    calculate_magnitude_and_classify()