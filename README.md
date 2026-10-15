# Product Opportunity Intelligence System

A lightweight tool that helps small e-commerce sellers identify high-potential products using an explainable Opportunity Score and review sentiment analysis.

## Features
- Relational database design using SQLite (Products and Reviews tables)
- Explainable Opportunity Score based on demand, competition, and rating
- Sentiment analysis on customer reviews using TextBlob
- Interactive Streamlit dashboard with charts and insights
- Support for synthetic data and real Amazon product data

## Project Structure
- `app.py` — Main Streamlit application
- `generate_data.py` — Generates synthetic product and review data
- `process_real_data.py` — Processes the Amazon Sales Dataset from Kaggle
- `requirements.txt` — Python dependencies

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/Deception94/product-opportunity-intelligence.git
cd product-opportunity-intelligence
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Generate synthetic data:
```bash
python generate_data.py
```

5. Run the application:
```bash
streamlit run app.py
```

The dashboard will open in your browser with synthetic data loaded by default.

## Using Real Amazon Data

1. Download the [Amazon Sales Dataset](https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset) from Kaggle and place `amazon.csv` in the project folder.
2. Run the processing script:
```bash
python process_real_data.py
```
3. In the Streamlit app, click **Load Sample Data** to load the real data.

## Opportunity Score Formula
```
Opportunity Score = 0.40 × Demand Score + 0.35 × (10 - Competition Score) + 0.25 × (Avg Rating × 2)
```

## Technologies Used
- Python
- SQLite
- Streamlit
- Pandas
- Plotly
- TextBlob

## Authors
Developed as a Database Systems and Data Mining project.
