import csv
from pathlib import Path
from typing import Dict, List

class ResultsWriter:
    """Tool to write candidate evaluation results to CSV."""
    
    def __init__(self, output_file: str):
        """Initialize the ResultsWriter with output file path."""
        self.output_file = output_file
        self.fieldnames = [
            'id',
            'name',
            'email',
            'assessment',
            'skills_match',
            'experience_match',
            'key_strengths',
            'concerns',
            'recommendation'
        ]
        self._initialize_csv()
    
    def _initialize_csv(self):
        """Create CSV file with headers if it doesn't exist."""
        Path(self.output_file).parent.mkdir(parents=True, exist_ok=True)
        if not Path(self.output_file).exists():
            with open(self.output_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
    
    def append_result(self, result: Dict):
        """Append a candidate evaluation result to the CSV file."""
        # Ensure all required fields exist
        for field in self.fieldnames:
            if field not in result:
                result[field] = ''
        
        # Write only the fields we want
        with open(self.output_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow({field: result[field] for field in self.fieldnames})

    def write_results(self, results: List[Dict]) -> None:
        """Write screening results to CSV file."""
        # Ensure directory exists
        Path(self.output_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Write results
        with open(self.output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'name',
                'email',
                'assessment',
                'skills_match',
                'experience_match',
                'strengths',
                'concerns',
                'recommendation'
            ])
            writer.writeheader()
            
            for result in results:
                # Add UUID if not present
                if 'id' not in result:
                    result['id'] = str(uuid.uuid4())
                
                # Ensure all fields exist
                for field in ['name', 'email', 'assessment', 'skills_match', 'experience_match', 'strengths', 'concerns', 'recommendation']:
                    if field not in result:
                        result[field] = ''
                
                writer.writerow(result) 