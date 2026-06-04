import streamlit as st
import pickle
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Finance Intelligence Pro",
    page_icon="💰",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("savings_model.pkl", "rb"))

# ---------------- CUSTOM CSS (DARK FINTECH UI) ----------------
st.markdown("""
<style>

body {
    background-color: #0b0f19;
}

.main {
    background-color: #0b0f19;
    color: white;
}

/* Title */
h1 {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg,#00FFB2,#00C9FF,#A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #aab0c0;
    margin-bottom: 25px;
}

/* Cards */
.card {
    background: #111827;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}

/* Metric boxes */
.metric {
    background: linear-gradient(135deg,#0ea5e9,#22c55e);
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    color: black;
    font-weight: bold;
}

/* Button */
.stButton > button {
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    background: linear-gradient(90deg,#00FFB2,#00C9FF);
    color: black;
    font-weight: bold;
    border: none;
    font-size: 16px;
}

.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 15px rgba(0,255,200,0.4);
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("# 💰 Finance Intelligence Pro")
st.markdown("<div class='subtitle'>AI-powered savings prediction & expense intelligence dashboard</div>", unsafe_allow_html=True)

# ---------------- INPUT SECTION ----------------
st.markdown("## 📋 User Financial Input")

col1, col2, col3 = st.columns(3)

with col1:
    income = st.number_input("Income", 1000, 500000, 50000)
    age = st.number_input("Age", 18, 80, 25)
    dependents = st.number_input("Dependents", 0, 10, 1)

with col2:
    rent = st.number_input("Rent", 0, 100000, 10000)
    loan = st.number_input("Loan", 0, 100000, 5000)
    insurance = st.number_input("Insurance", 0, 50000, 2000)

with col3:
    groceries = st.number_input("Groceries", 0, 50000, 5000)
    transport = st.number_input("Transport", 0, 50000, 3000)
    eating = st.number_input("Eating Out", 0, 50000, 2000)

# ---------------- BUTTON ----------------
st.markdown("---")
predict = st.button("🚀 Analyze Financial Health")

# ---------------- PREDICTION ----------------
if predict:

    X = [[
        income, age, dependents,
        rent, loan, insurance,
        groceries, transport, eating,
        2000, 3000, 2000,
        2000, 1000
    ]]

    savings = float(model.predict(X)[0])
    total_expenses = rent + loan + insurance + groceries + transport + eating
    score = (savings / income) * 100 if income > 0 else 0

    # ---------------- METRICS ROW ----------------
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric">
        💰 Income<br><h2>₹{income:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric">
        🪙 Savings<br><h2>₹{savings:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric">
        📊 Health Score<br><h2>{score:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ---------------- STATUS ----------------
    if score >= 30:
        st.success("🟢 Excellent Financial Health")
    elif score >= 15:
        st.warning("🟡 Moderate Financial Health")
    else:
        st.error("🔴 Poor Financial Health")

    # ---------------- AI INSIGHTS ----------------
    st.markdown("## 🤖 AI Insights")

    insights = []

    if groceries > 8000:
        insights.append("Reduce grocery spending")
    if eating > 4000:
        insights.append("Reduce eating out")
    if loan > 15000:
        insights.append("Reduce loan burden")
    if score < 20:
        insights.append("Increase savings rate")

    if not insights:
        insights.append("Great financial discipline 👍")

    for i in insights:
        st.info("💡 " + i)

    # ---------------- CHART DATA ----------------
    data = pd.DataFrame({
        "Category": ["Rent","Loan","Insurance","Groceries","Transport","Eating"],
        "Amount": [rent, loan, insurance, groceries, transport, eating]
    })

    st.markdown("## 📊 Expense Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Expense Pie Chart")
        fig = px.pie(data, names="Category", values="Amount", hole=0.5)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Expense Bar Chart")
        fig2 = px.bar(data, x="Category", y="Amount")
        st.plotly_chart(fig2, use_container_width=True)