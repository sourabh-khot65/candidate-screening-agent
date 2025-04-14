import pandas as pd
from pathlib import Path

def load_candidates():
    """
    Load candidate data from CSV file.
    Returns a pandas DataFrame containing candidate information.
    """
    data_path = Path(__file__).parent / "data" / "candidates.csv"
    return pd.read_csv(data_path)

def get_candidate_by_id(candidate_id):
    """
    Retrieve candidate information by their ID.
    Args:
        candidate_id (int): The ID of the candidate to look up
    Returns:
        dict: Candidate information or None if not found
    """
    df = load_candidates()
    candidate = df[df['id'] == candidate_id]
    return candidate.to_dict('records')[0] if not candidate.empty else None

def get_all_candidates():
    """
    Retrieve all candidates.
    Returns:
        list: List of dictionaries containing candidate information
    """
    df = load_candidates()
    return df.to_dict('records')

if __name__ == "__main__":
    # Example usage
    print("All candidates:")
    candidates = get_all_candidates()
    for candidate in candidates:
        print(f"ID: {candidate['id']}, Name: {candidate['name']}, Email: {candidate['email']}") 