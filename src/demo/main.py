#!/usr/bin/env python
import sys
import warnings
import csv
from pathlib import Path
from datetime import datetime

try:
    from .crew import Demo
except ImportError:
    from demo.crew import Demo

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def load_candidate_data(file_path: str) -> dict:
    """Load candidate data from CSV file."""
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        return dict(reader)

def run():
    """
    Run the candidate screening crew.
    """
    try:
        # Load candidate data
        candidate_file = Path(__file__).parent / "data" / "candidate.csv"
        candidate_data = load_candidate_data(str(candidate_file))
        
        inputs = {
            'candidate': candidate_data,
            'position': 'Senior Software Engineer',
            'current_year': str(datetime.now().year)
        }
        
        result = Demo().crew().kickoff(inputs=inputs)
        print("\n=== Screening Results ===")
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        candidate_file = Path(__file__).parent / "data" / "candidate.csv"
        candidate_data = load_candidate_data(str(candidate_file))
        
        inputs = {
            'candidate': candidate_data,
            'position': 'Senior Software Engineer'
        }
        Demo().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Demo().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    try:
        candidate_file = Path(__file__).parent / "data" / "candidate.csv"
        candidate_data = load_candidate_data(str(candidate_file))
        
        inputs = {
            'candidate': candidate_data,
            'position': 'Senior Software Engineer',
            'current_year': str(datetime.now().year)
        }
        Demo().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()
