import pandas as pd
from pathlib import Path

def load_candidates():
    """
    Load candidates data from CSV file
    Returns: pandas DataFrame containing candidate information
    """
    data_path = Path('data/candidates.csv')
    return pd.read_csv(data_path)

def filter_by_skill(df, skill):
    """
    Filter candidates by a specific skill
    Args:
        df: pandas DataFrame containing candidate data
        skill: skill to filter by
    Returns: filtered DataFrame
    """
    return df[df['skills'].str.contains(skill, case=False)]

def get_experienced_candidates(df, min_years):
    """
    Get candidates with experience above specified years
    Args:
        df: pandas DataFrame containing candidate data
        min_years: minimum years of experience required
    Returns: filtered DataFrame
    """
    return df[df['experience_years'] >= min_years]

if __name__ == '__main__':
    # Load the data
    candidates_df = load_candidates()
    
    # Example usage
    print("\nAll Candidates:")
    print(candidates_df)
    
    print("\nPython Developers:")
    python_devs = filter_by_skill(candidates_df, 'Python')
    print(python_devs)
    
    print("\nCandidates with 5+ years experience:")
    experienced = get_experienced_candidates(candidates_df, 5)
    print(experienced) 