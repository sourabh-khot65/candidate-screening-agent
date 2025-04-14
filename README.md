# Candidate Data Processing

This project provides utilities for processing candidate data from a CSV file. It includes functionality to filter candidates by skills and experience level.

## Features

- Load candidate data from CSV
- Filter candidates by specific skills (case-insensitive)
- Get candidates with minimum years of experience
- Easy to extend with additional filtering capabilities

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Place your candidate data in `data/candidates.csv` with the following columns:
   - id
   - name
   - email
   - resume_url

## Usage

```python
from src.process_candidates import load_candidates, filter_by_skill, get_experienced_candidates

# Load all candidates
df = load_candidates()

# Filter Python developers
python_devs = filter_by_skill(df, "Python")

# Get candidates with 5+ years experience
experienced = get_experienced_candidates(df, 5)
```

## Project Structure

```
.
├── data/
│   └── candidates.csv
├── src/
│   └── process_candidates.py
├── requirements.txt
└── README.md
```
