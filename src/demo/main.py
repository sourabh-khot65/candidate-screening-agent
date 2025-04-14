#!/usr/bin/env python
import sys
import warnings
from pathlib import Path
from datetime import datetime

from demo.crew import Demo
from demo.tools.resume_fetcher import ResumeFetcher
from demo.tools.results_writer import ResultsWriter

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def read_job_description(file_path: str) -> str:
    """Read job description from file."""
    with open(file_path, 'r') as f:
        return f.read()

def parse_crew_output(output_text: str) -> dict:
    """Parse the crew output text into a structured format."""
    try:
        lines = output_text.split('\n')
        result = {
            'assessment': 'Consider',
            'skills_match': '0%',
            'experience_match': '0%',
            'key_strengths': '',
            'concerns': '',
            'recommendation': ''
        }
        
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if "Overall Assessment:" in line:
                result['assessment'] = line.split(':')[1].strip()
            elif "Technical Skills Match:" in line:
                result['skills_match'] = line.split(':')[1].strip()
            elif "Experience Match:" in line:
                result['experience_match'] = line.split(':')[1].strip()
            elif "Key Strengths:" in line:
                current_section = 'strengths'
                result['key_strengths'] = ''
            elif "Areas of Concern:" in line:
                current_section = 'concerns'
                result['concerns'] = ''
            elif "Final Recommendation:" in line:
                current_section = None
                result['recommendation'] = line.split(':')[1].strip()
            elif current_section:
                if current_section == 'strengths':
                    result['key_strengths'] += line + '; '
                elif current_section == 'concerns':
                    result['concerns'] += line + '; '
                
        # Clean up the lists
        result['key_strengths'] = result['key_strengths'].strip('; ')
        result['concerns'] = result['concerns'].strip('; ')
                
        return result
    except Exception as e:
        print(f"Error parsing crew output: {e}")
        return {
            'assessment': 'Error',
            'skills_match': '0%',
            'experience_match': '0%',
            'key_strengths': 'Error parsing output',
            'concerns': 'Error parsing output',
            'recommendation': 'Error in evaluation'
        }

def run():
    """
    Run the candidate evaluation crew.
    """
    try:
        # Initialize tools
        fetcher = ResumeFetcher()
        writer = ResultsWriter(output_file=str(Path(__file__).parent / "data" / "result.csv"))
        
        # Read job description
        job_desc_path = str(Path(__file__).parent / "data" / "job_description.txt")
        job_description = read_job_description(job_desc_path)
        
        # Process candidates
        candidates_file = str(Path(__file__).parent / "data" / "candidates.csv")
        candidates = fetcher.process_candidates(candidates_file)
        
        print(f"\nEvaluating {len(candidates)} candidates...")
        
        # Process each candidate
        for candidate in candidates:
            print(f"\nEvaluating {candidate['name']}...")
            
            inputs = {
                'candidate': candidate,
                'position': 'Senior Android Developer',
                'job_description': job_description
            }
            
            # Run crew analysis
            result = Demo().crew().kickoff(inputs=inputs)
            
            # Parse the crew output
            evaluation_result = parse_crew_output(str(result))
            
            # Create the evaluation result
            final_result = {
                'id': candidate['id'],
                'name': candidate['name'],
                'email': candidate['email'],
                **evaluation_result
            }
            
            # Write result
            writer.append_result(final_result)
            
            print(f"Completed evaluation for {candidate['name']}")
            print(f"Assessment: {evaluation_result['assessment']}")
            print(f"Skills Match: {evaluation_result['skills_match']}")
            print(f"Experience Match: {evaluation_result['experience_match']}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        raise Exception(f"An error occurred while evaluating candidates: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        # Similar setup as run()
        fetcher = ResumeFetcher()
        candidates_file = str(Path(__file__).parent / "data" / "candidates.csv")
        candidates = fetcher.process_candidates(candidates_file)
        
        if candidates:
            inputs = {
                'candidate': candidates[0],
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
        # Similar setup as run()
        fetcher = ResumeFetcher()
        candidates_file = str(Path(__file__).parent / "data" / "candidates.csv")
        candidates = fetcher.process_candidates(candidates_file)
        
        if candidates:
            inputs = {
                'candidate': candidates[0],  # Use first candidate for testing
                'position': 'Senior Software Engineer',
                'current_year': str(datetime.now().year)
            }
            Demo().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()
