
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("📊 PhonePe Transaction Insights Dashboard")

# Connect to database
conn = sqlite3.connect("phonepe.db")

# Sidebar
st.sidebar.header("Navigation")
section = st.sidebar.radio("Go to:", ["Overview", "State Analysis", "Yearly Trends", "Top Districts & Pincodes", "Insurance Trends"])

# Overview
if section == "Overview":
    st.header("Project Summary")
    st.markdown("""
    - 📁 **Data Source**: PhonePe Pulse Dataset
    - 🛠️ **Tools**: Python, SQLite, Pandas, Seaborn, Streamlit
    - 📌 **Goal**: Analyze digital payment patterns across India from 2018 to 2024
    - 📍 Focused on: Transaction Volume, User Growth, Insurance Adoption, Geographic Trends
    """)

# State-wise Transaction Amounts
elif section == "State Analysis":
    st.header("📍 State-wise Transaction Amounts")
    query = "SELECT State, SUM(Transaction_amount) as total_amount FROM Aggregated_transaction GROUP BY State ORDER BY total_amount DESC;"
    df_state = pd.read_sql_query(query, conn)

    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(data=df_state.head(10), x="State", y="total_amount", palette="viridis", ax=ax)
    plt.xticks(rotation=45)
    plt.title("Top 10 States by Transaction Amount")
    st.pyplot(fig)

# Yearly Transaction Trends
elif section == "Yearly Trends":
    st.header("📅 Yearly Transaction Amount Trends")
    query = "SELECT Year, SUM(Transaction_amount) as total_amount FROM Aggregated_transaction GROUP BY Year ORDER BY Year;"
    df_year = pd.read_sql_query(query, conn)

    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(data=df_year, x="Year", y="total_amount", marker="o", ax=ax)
    plt.title("Year-wise Total Transaction Amount")
    st.pyplot(fig)

# Top Districts and Pincodes
elif section == "Top Districts & Pincodes":
    st.header("🏙️ Top Districts by Transaction")
    query1 = "SELECT District_or_Pincode, SUM(Transaction_amount) AS total_amount FROM Top_transaction GROUP BY District_or_Pincode ORDER BY total_amount DESC LIMIT 10;"
    df_dist = pd.read_sql_query(query1, conn)
    st.dataframe(df_dist)

    st.header("📮 Top Pincodes by Registered Users")
    query2 = "SELECT Pincode, SUM(RegisteredUsers) AS total_users FROM Top_user GROUP BY Pincode ORDER BY total_users DESC LIMIT 10;"
    df_pin = pd.read_sql_query(query2, conn)
    st.dataframe(df_pin)

# Insurance Trends
# Insurance Trends
elif section == "Insurance Trends":
    st.header("📈 Quarterly Insurance Amount Trends")
    
    query = '''
    SELECT Year, Quarter, SUM(Insurance_amount) AS total_insurance_amount
    FROM Aggregated_insurance
    GROUP BY Year, Quarter
    ORDER BY Year, Quarter;
    '''
    
    df_ins = pd.read_sql_query(query, conn)

    # Create Year_Quarter column for better x-axis labels
    df_ins["Year_Quarter"] = df_ins["Year"].astype(str) + " Q" + df_ins["Quarter"].astype(str)

    fig, ax = plt.subplots(figsize=(14,6))
    sns.lineplot(data=df_ins, x="Year_Quarter", y="total_insurance_amount", marker="o", ax=ax, color='teal')
    plt.xticks(rotation=45)
    plt.title("Quarter-wise Insurance Transactions Over Years")
    plt.ylabel("Total Insurance Amount")
    plt.xlabel("Year & Quarter")
    st.pyplot(fig)

conn.close()
