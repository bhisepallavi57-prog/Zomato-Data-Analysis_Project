# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="Zomato Dashboard",
    layout="wide"
)

# =========================
# Title
# =========================

st.title("🍽️ Zomato Data Analysis Dashboard")

st.markdown("Analyze restaurant ratings, votes, costs and ordering trends")

# =========================
# Load Dataset
# =========================

df = pd.read_csv("Zomato data .csv")

# =========================
# Data Cleaning
# =========================

# Clean rating column
df['rate'] = df['rate'].str.replace('/5', '')

df['rate'] = pd.to_numeric(
    df['rate'],
    errors='coerce'
)

# Remove null values
df.dropna(inplace=True)

# =========================
# Sidebar Filters
# =========================

st.sidebar.header("Filter Options")

# Restaurant Type Filter
restaurant_type = st.sidebar.multiselect(
    "Select Restaurant Type",
    options=df['listed_in(type)'].unique(),
    default=df['listed_in(type)'].unique()
)

# Online Order Filter
online_order = st.sidebar.multiselect(
    "Online Order",
    options=df['online_order'].unique(),
    default=df['online_order'].unique()
)

# Table Booking Filter
book_table = st.sidebar.multiselect(
    "Table Booking",
    options=df['book_table'].unique(),
    default=df['book_table'].unique()
)

# =========================
# Filter Dataset
# =========================

filtered_df = df[
    (df['listed_in(type)'].isin(restaurant_type)) &
    (df['online_order'].isin(online_order)) &
    (df['book_table'].isin(book_table))
]

# =========================
# Dataset Preview
# =========================

st.subheader("📄 Dataset Preview")

st.dataframe(filtered_df.head())

# =========================
# KPI Section
# =========================

st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Restaurants",
    filtered_df.shape[0]
)

col2.metric(
    "Average Rating",
    round(filtered_df['rate'].mean(), 2)
)

col3.metric(
    "Average Votes",
    int(filtered_df['votes'].mean())
)

col4.metric(
    "Average Cost",
    int(filtered_df[
        'approx_cost(for two people)'
    ].mean())
)

# =========================
# Restaurant Type Analysis
# =========================

st.subheader("🍴 Restaurant Type Analysis")

fig1, ax1 = plt.subplots(figsize=(10, 5))

sns.countplot(
    x='listed_in(type)',
    data=filtered_df,
    ax=ax1
)

plt.xticks(rotation=45)

st.pyplot(fig1)

# =========================
# Ratings Distribution
# =========================

st.subheader("⭐ Ratings Distribution")

fig2, ax2 = plt.subplots(figsize=(10, 5))

sns.histplot(
    filtered_df['rate'],
    bins=10,
    kde=True,
    ax=ax2
)

st.pyplot(fig2)

# =========================
# Online Order Analysis
# =========================

st.subheader("🛒 Online Order Analysis")

fig3, ax3 = plt.subplots(figsize=(6, 5))

sns.countplot(
    x='online_order',
    data=filtered_df,
    ax=ax3
)

st.pyplot(fig3)

# =========================
# Table Booking Analysis
# =========================

st.subheader("📅 Table Booking Analysis")


fig4, ax4 = plt.subplots(figsize=(6, 5))

sns.countplot(
    x='book_table',
    data=filtered_df,
    ax=ax4
)

st.pyplot(fig4)

# =========================
# Top Restaurants by Votes
# =========================

st.subheader("🏆 Top 10 Restaurants by Votes")

top_votes = filtered_df.sort_values(
    by='votes',
    ascending=False
).head(10)

fig5, ax5 = plt.subplots(figsize=(12, 6))

sns.barplot(
    x='votes',
    y='name',
    data=top_votes,
    ax=ax5
)

st.pyplot(fig5)

# =========================
# Online Order vs Rating
# =========================

st.subheader("📈 Online Order vs Ratings")

fig6, ax6 = plt.subplots(figsize=(7, 5))

sns.boxplot(
    x='online_order',
    y='rate',
    data=filtered_df,
    ax=ax6
)

st.pyplot(fig6)

# =========================
# Cost Distribution
# =========================

st.subheader("💰 Cost Distribution")

fig7, ax7 = plt.subplots(figsize=(8, 5))

sns.histplot(
    filtered_df['approx_cost(for two people)'],
    bins=15,
    kde=True,
    ax=ax7
)

st.pyplot(fig7)

# =========================
# Correlation Heatmap
# =========================

st.subheader("🔥 Correlation Heatmap")

numeric_df = filtered_df[
    [
        'rate',
        'votes',
        'approx_cost(for two people)'
    ]
]

correlation = numeric_df.corr()

fig8, ax8 = plt.subplots(figsize=(6, 4))

sns.heatmap(
    correlation,
    annot=True,
    cmap='coolwarm',
    ax=ax8
)

st.pyplot(fig8)

# =========================
# Raw Dataset
# =========================

st.subheader("🗂️ Complete Dataset")

st.dataframe(filtered_df)

# =========================
# Footer
# =========================

st.markdown("---")

st.markdown(
    "✅ Developed using Python, Pandas, Seaborn and Streamlit"
)