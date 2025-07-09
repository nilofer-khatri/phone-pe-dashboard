
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
section = st.sidebar.radio("Go to:", ["Overview", "State Analysis", "Yearly Trends", "Top Districts & Pincodes", "Insurance Trends", "Customer Segmentation"])


# Overview
if section == "Overview":
    st.header("Project Summary")
    st.markdown("""
    - 📁 **Data Source**: PhonePe Pulse Dataset
    - 🛠️ **Tools**: Python, SQLite, Pandas, Seaborn, Streamlit
    - 📌 **Goal**: Analyze digital payment patterns across India from 2018 to 2024
    - 📍 Focused on: Transaction Volume, User Growth, Insurance Adoption, Geographic Trends
    """)

    st.markdown("### 🔍 Insights")
    st.write("- Digital payments in India have grown rapidly with UPI platforms like PhonePe.")
    st.write("- This dashboard helps explore geographic and temporal patterns of transactions and insurance.")


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

    st.markdown("### 🔍 Insights")
    st.write("- Maharashtra, Karnataka, and Telangana lead in digital transactions.")
    st.write("- These states reflect better digital adoption and payment infrastructure.")


# Yearly Transaction Trends
elif section == "Yearly Trends":
    st.header("📅 Yearly Transaction Amount Trends")
    query = "SELECT Year, SUM(Transaction_amount) as total_amount FROM Aggregated_transaction GROUP BY Year ORDER BY Year;"
    df_year = pd.read_sql_query(query, conn)

    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(data=df_year, x="Year", y="total_amount", marker="o", ax=ax)
    plt.title("Year-wise Total Transaction Amount")
    st.pyplot(fig)

    st.markdown("### 🔍 Insights")
    st.write("- Transaction volume grew significantly from 2018 to 2024.")
    st.write("- A visible spike post-2020 shows increased digital usage during and after the pandemic.")


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

    st.markdown("### 🔍 Insights")
    st.write("- Districts from metro areas like Mumbai and Bengaluru show the highest digital activity.")
    st.write("- Pincodes with more registered users point to urban centers with higher smartphone penetration.")


# Insurance Trends
elif section == "Insurance Trends":
    st.header("📈 Quarterly Insurance Amount Trends")

    # Quarter filter dropdown
    selected_year = st.selectbox("Select Year", sorted(df_ins["Year"].unique()))
    selected_quarter = st.selectbox("Select Quarter", sorted(df_ins["Quarter"].unique()))

    # Filter the data
    query = f"""
        SELECT Year, Quarter, SUM(Insurance_amount) AS total_insurance_amount
        FROM Aggregated_insurance
        WHERE Year = {selected_year} AND Quarter = {selected_quarter}
        GROUP BY Year, Quarter
        ORDER BY Year, Quarter;
    """
    df_filtered = pd.read_sql_query(query, conn)

    # Show filtered line chart
    df_filtered["Year_Quarter"] = df_filtered["Year"].astype(str) + " Q" + df_filtered["Quarter"].astype(str)

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=df_filtered, x="Year_Quarter", y="total_insurance_amount", palette="coolwarm", ax=ax)
    plt.title(f"Insurance Transactions: {selected_year} Q{selected_quarter}")
    st.pyplot(fig)


    # Create Year_Quarter column for better x-axis labels
    df_ins["Year_Quarter"] = df_ins["Year"].astype(str) + " Q" + df_ins["Quarter"].astype(str)

    fig, ax = plt.subplots(figsize=(14,6))
    sns.lineplot(data=df_ins, x="Year_Quarter", y="total_insurance_amount", marker="o", ax=ax, color='teal')
    plt.xticks(rotation=45)
    plt.title("Quarter-wise Insurance Transactions Over Years")
    plt.ylabel("Total Insurance Amount")
    plt.xlabel("Year & Quarter")
    st.pyplot(fig)

    st.markdown("### 🔍 Insights")
    st.write("- Steady growth in digital insurance adoption since 2021.")
    st.write("- Urban regions show strong trust in digital financial services.")
    st.write("- Peaks in specific quarters indicate seasonal campaigns or awareness drives.")


# Customer Segmentation
elif section == "Customer Segmentation":
    st.header("👥 Customer Segmentation by State and Year")

    # Filters
    state_options = pd.read_sql_query("SELECT DISTINCT State FROM Top_user", conn)
    year_options = pd.read_sql_query("SELECT DISTINCT Year FROM Top_user", conn)

    selected_state = st.selectbox("Select State", sorted(state_options["State"].unique()))
    selected_year = st.selectbox("Select Year", sorted(year_options["Year"].unique()))

    # Query filtered data
    query = f'''
        SELECT State, Year, Pincode, RegisteredUsers, AppOpens
        FROM Top_user
        WHERE State = '{selected_state}' AND Year = {selected_year}
        ORDER BY RegisteredUsers DESC
        LIMIT 10;
    '''
    df_segment = pd.read_sql_query(query, conn)

    # Display data
    st.dataframe(df_segment)

    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=df_segment, x="Pincode", y="RegisteredUsers", palette="mako", ax=ax)
    plt.xticks(rotation=45)
    plt.title(f"Top 10 Pincodes by Registered Users in {selected_state} ({selected_year})")
    st.pyplot(fig)

    # Insights
    st.markdown("### 🔍 Insights")
    st.write(f"- In {selected_state}, users in certain pincodes are highly active with many registrations.")
    st.write("- Regions with high registrations can be targeted for new product launches or awareness campaigns.")



   


conn.close()
