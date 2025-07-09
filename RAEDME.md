# 📊 PhonePe Transaction Insights Dashboard

An interactive dashboard built with **Python**, **SQLite**, and **Streamlit** to explore digital payment trends across India using the **PhonePe Pulse dataset**.

---

## 📁 Dataset
- **Source:** [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse)
- Covers **digital transactions** from 2018 to 2024
- Includes: Transactions, Users, Insurance, States, Districts, Pincodes

---

## 💻 Tools & Technologies Used
- **Python**
- **Pandas, Seaborn, Matplotlib**
- **SQLite**
- **Streamlit** for the dashboard
- **Git & GitHub** for version control

---

## 🎯 Project Objective
To analyze and visualize PhonePe transaction data to extract:
- Customer Segmentation by State and Year
- Payment Category Trends
- Insurance Product Growth
- Top Districts and Pincodes
- Yearly and Quarterly Payment Trends

---

## 🧠 Key Business Use Cases
- 🔍 **Customer Segmentation:** Understand regional and time-based transaction patterns  
- 🛡️ **Insurance Insights:** Identify adoption trends in digital insurance  
- 🗺️ **Geographic Trends:** Discover top-performing states and districts  
- 📈 **Trend Analysis:** Monitor growth over years and quarters  
- 🛠️ **Product Strategy:** Suggest new features based on user behavior  

---

## 📌 Dashboard Features (Streamlit)
- Sidebar navigation for multiple pages:
  - Overview
  - State Analysis
  - Yearly Trends
  - Top Districts & Pincodes
  - Insurance Trends
  - **Customer Segmentation**
- Dropdown filters for **state** and **year**
- Interactive visualizations (bar charts, line plots)

---

## 📷 Dashboard Preview
![Dashboard Screenshot](preview-image-url-if-any)

---

## 🧪 How to Run the Project Locally

```bash
# Clone the repo
git clone https://github.com/nilofer-khatri/phone-pe-dashboard.git
cd phone-pe-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
