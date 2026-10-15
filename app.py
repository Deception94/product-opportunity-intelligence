import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from textblob import TextBlob
import os

st.set_page_config(
    page_title="Product Opportunity Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4b5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e40af;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6b7280;
        margin-top: 0.3rem;
    }
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1f2937;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #3b82f6;
        padding-left: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🛒 Product Opportunity Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Find high-potential products for small e-commerce sellers using demand, competition, and review insights</div>', unsafe_allow_html=True)

DB_PATH = "opportunity.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            price REAL,
            avg_rating REAL,
            review_count INTEGER,
            competition_score REAL,
            demand_score REAL,
            opportunity_score REAL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY,
            product_id INTEGER,
            rating INTEGER,
            review_text TEXT,
            review_date TEXT,
            sentiment REAL,
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    """)
    conn.commit()
    conn.close()

def load_data_to_db(products_df, reviews_df):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM reviews")
    conn.execute("DELETE FROM products")
    
    products_df = products_df.copy()
    products_df["opportunity_score"] = (
        (products_df["demand_score"] * 0.4) +
        ((10 - products_df["competition_score"]) * 0.35) +
        (products_df["avg_rating"] * 2 * 0.25)
    ).round(2)
    
    products_df.to_sql("products", conn, if_exists="append", index=False)
    
    reviews_df = reviews_df.copy()
    reviews_df["sentiment"] = reviews_df["review_text"].apply(
        lambda x: round(TextBlob(str(x)).sentiment.polarity, 3)
    )
    reviews_df.to_sql("reviews", conn, if_exists="append", index=False)
    conn.close()

def get_data():
    conn = sqlite3.connect(DB_PATH)
    products = pd.read_sql("SELECT * FROM products", conn)
    reviews = pd.read_sql("SELECT * FROM reviews", conn)
    conn.close()
    return products, reviews

init_db()

# Auto-load synthetic data on first run
if not os.path.exists(DB_PATH) or os.path.getsize(DB_PATH) == 0:
    try:
        products_df = pd.read_csv("products.csv")
        reviews_df = pd.read_csv("reviews.csv")
        load_data_to_db(products_df, reviews_df)
    except:
        pass

with st.sidebar:
    st.header("📁 Data Source")
    use_sample = st.button("Load Sample Data", type="primary", use_container_width=True)
    st.markdown("---")
    st.caption("Opportunity Score = 40% Demand + 35% Low Competition + 25% Rating")

if use_sample:
    try:
        products_df = pd.read_csv("real_products.csv")
        reviews_df = pd.read_csv("real_reviews.csv")
        load_data_to_db(products_df, reviews_df)
        st.sidebar.success("Sample data loaded successfully!")
        st.rerun()
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

products, reviews = get_data()

if products.empty:
    st.info("👈 Click 'Load Sample Data' in the sidebar to begin.")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(products)}</div><div class="metric-label">Total Products</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{products["opportunity_score"].mean():.2f}</div><div class="metric-label">Avg Opportunity Score</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{products["avg_rating"].mean():.2f}</div><div class="metric-label">Avg Rating</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(reviews)}</div><div class="metric-label">Total Reviews</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">🏆 Top Product Opportunities</div>', unsafe_allow_html=True)
    top = products.nlargest(10, "opportunity_score")[
        ["product_name", "category", "price", "avg_rating", "demand_score", "competition_score", "opportunity_score"]
    ]
    st.dataframe(
        top.style.background_gradient(subset=["opportunity_score"], cmap="Greens").format({
            "price": "₹{:.0f}",
            "avg_rating": "{:.1f}",
            "demand_score": "{:.1f}",
            "competition_score": "{:.1f}",
            "opportunity_score": "{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-title">Demand vs Competition</div>', unsafe_allow_html=True)
        fig = px.scatter(
            products, x="competition_score", y="demand_score",
            size="review_count", color="opportunity_score",
            hover_name="product_name",
            color_continuous_scale="Blues",
            labels={"competition_score": "Competition Score", "demand_score": "Demand Score"}
        )
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title">Opportunity by Category</div>', unsafe_allow_html=True)
        cat_data = products.groupby("category")["opportunity_score"].mean().reset_index()
        cat_data = cat_data.sort_values("opportunity_score", ascending=False).head(10)
        fig2 = px.bar(
            cat_data, x="category", y="opportunity_score",
            color="opportunity_score", color_continuous_scale="Blues"
        )
        fig2.update_layout(
            height=400, 
            margin=dict(l=20, r=20, t=30, b=20), 
            showlegend=False,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-title">📝 Review Sentiment Insights</div>', unsafe_allow_html=True)
    if not reviews.empty:
        avg_sent = reviews.groupby("product_id")["sentiment"].mean().reset_index()
        merged = products.merge(avg_sent, on="product_id", how="left")

        fig3 = px.histogram(
            merged, x="sentiment", nbins=25,
            labels={"sentiment": "Average Sentiment Score"}
        )
        fig3.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig3, use_container_width=True)

        negative = reviews[reviews["sentiment"] < -0.1]
        if not negative.empty:
            st.markdown("**Common Issues from Negative Reviews:**")
            neg_with_product = negative.merge(
                products[["product_id", "product_name"]], 
                on="product_id", 
                how="left"
            )
            sample_neg = neg_with_product.sample(min(5, len(neg_with_product)))
            for _, row in sample_neg.iterrows():
                st.markdown(f"- **{row['product_name']}**: *{row['review_text']}* (Rating: {row['rating']})")
