import requests
from pathlib import Path
import csv
from typing import Dict, List
import markdown
from bs4 import BeautifulSoup
import io
import pandas as pd
from PyPDF2 import PdfReader

class ResumeFetcher:
    """Tool to fetch and parse resumes from URLs."""
    
    @staticmethod
    def fetch_content(url: str) -> str:
        """Fetch content from URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            # extract the text from reponse file 
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            return text
        except Exception as e:
            print(f"Error fetching URL {url}: {str(e)}")
            return ""

            print(f"Error fetching URL {url}: {str(e)}")
            return ""

    @staticmethod
    def parse_markdown(content: str) -> str:
        """Parse markdown content to plain text."""
        # Convert markdown to HTML
        html = markdown.markdown(content)
        # Convert HTML to plain text
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()

    @staticmethod
    def extract_social_links(text: str) -> Dict[str, str]:
        """Extract social media and portfolio links from text."""
        links = {
            'github': '',
            'linkedin': '',
            'portfolio': ''
        }
        
        lines = text.lower().split('\n')
        for line in lines:
            if 'github.com' in line:
                links['github'] = line.split('github.com/')[-1].strip()
            elif 'linkedin.com' in line:
                links['linkedin'] = line.split('linkedin.com/in/')[-1].strip()
            elif any(domain in line for domain in ['.dev', '.io', '.com']) and 'portfolio' not in links:
                links['portfolio'] = line.strip()
                
        return links

    @staticmethod
    def load_candidates(file_path: str) -> List[Dict]:
        """Load candidates from CSV file."""
        candidates = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                candidates.append(row)
        return candidates

    def process_candidates(self, candidates_file: str) -> list:
        """Process candidates from CSV file and fetch their resumes."""
        df = pd.read_csv(candidates_file)
        candidates = []
        
        for _, row in df.iterrows():
            try:
                resume_text = self._fetch_and_read_pdf(row['resume_url'])
                candidates.append({
                    'id': row['id'],
                    'name': row['name'],
                    'email': row['email'],
                    'resume_text': resume_text
                })
                print(f"Successfully processed resume for {row['name']}")
            except Exception as e:
                print(f"Error processing resume for {row['name']}: {str(e)}")
                continue
                
        return candidates

    def _fetch_and_read_pdf(self, url: str) -> str:
        """Download PDF from URL and extract text."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            pdf_file = io.BytesIO(response.content)
            pdf_reader = PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
                
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Failed to process PDF: {str(e)}") 