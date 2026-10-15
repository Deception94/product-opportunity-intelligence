# Product Opportunity Intelligence System

A database-driven tool that helps small e-commerce sellers identify high-potential products using opportunity scoring and review sentiment analysis.

## Features
- SQLite database with Products and Reviews tables
- Explainable Opportunity Score (Demand + Low Competition + Rating)
- Sentiment analysis on reviews using TextBlob
- Interactive Streamlit dashboard
- Support for both synthetic and real Amazon data

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python generate_data.py
streamlit run app.py
```

## Real Data
Process the Amazon Sales Dataset from Kaggle using `process_real_data.py`.

## Research Paper
See `paper.tex` for the IEEE format research paper.
