import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="EnergiSense AI", layout="wide")

st.title("🌍 EnergiSense AI")
st.subheader("AI-Based Smart Energy Optimization System")

# ---------------- LOAD DATA ----------------
data = pd.read_csv("electricity_bill_dataset.csv")
data = pd.get_dummies(data)

X = data.drop("ElectricityBill", axis=1)
y = data["ElectricityBill"]

model = LinearRegression()
model.fit(X, y)

# ---------------- SIDEBAR INPUT ----------------
st.sidebar.header("Enter Appliance Usage")

fan = st.sidebar.number_input("Fan Units", 0, 10, 2)
ac = st.sidebar.number_input("AC Units", 0, 5, 1)
tv = st.sidebar.number_input("TV Units", 0, 5, 1)
fridge = st.sidebar.number_input("Refrigerator Units", 0, 3, 1)
washing = st.sidebar.number_input("Washing Machine Units", 0, 3, 1)

hours = st.sidebar.slider("Usage Hours per Day", 1, 24, 5)
tariff = st.sidebar.number_input("Tariff Rate (₹)", 1, 20, 8)

# ---------------- BUTTON ----------------
if st.button("Generate Report"):

    power = {
        "fan": 75,
        "ac": 1500,
        "tv": 120,
        "fridge": 200,
        "washing": 500
    }

    fan_energy = fan * power["fan"] * hours / 1000
    ac_energy = ac * power["ac"] * hours / 1000
    tv_energy = tv * power["tv"] * hours / 1000
    fridge_energy = fridge * power["fridge"] * hours / 1000
    washing_energy = washing * power["washing"] * hours / 1000

    daily_energy = fan_energy + ac_energy + tv_energy + fridge_energy + washing_energy
    monthly_energy = daily_energy * 30
    bill = monthly_energy * tariff

    st.header("📊 Energy Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Daily Energy (kWh)", round(daily_energy, 2))
    col2.metric("Monthly Energy (kWh)", round(monthly_energy, 2))
    col3.metric("Estimated Monthly Bill (₹)", round(bill, 2))

    energy_data = {
        "Appliance": ["Fan", "AC", "TV", "Fridge", "Washing Machine"],
        "Energy": [fan_energy, ac_energy, tv_energy, fridge_energy, washing_energy]
    }

    fig = px.pie(energy_data, names="Appliance", values="Energy")
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- ENERGY SCORE ----------------
    st.header("🤖 Energy Efficiency Score")

    score = 100
    if ac > 2:
        score -= 20
    if hours > 10:
        score -= 15
    if monthly_energy > 400:
        score -= 25

    st.metric("Energy Score", f"{score}/100")

    # ---------------- CARBON ----------------
    st.header("🌱 Carbon Footprint")

    carbon = monthly_energy * 0.82
    st.metric("Monthly CO₂ Emission (kg)", round(carbon, 2))

    # ---------------- IDLE DETECTION ----------------
    st.header("🛑 Idle Appliance Detection")

    idle_devices = []

    if fan > 0 and hours < 2:
        idle_devices.append("Fan")
    if ac > 0 and hours < 2:
        idle_devices.append("AC")
    if tv > 0 and hours < 2:
        idle_devices.append("TV")

    if idle_devices:
        st.warning("Idle Devices: " + ", ".join(idle_devices))
    else:
        st.success("No idle appliances detected")

    # ---------------- CLUSTERING ----------------
    st.header("🔵 Energy Usage Clustering")

    cluster_df = pd.DataFrame({
        "Energy": [fan_energy, ac_energy, tv_energy, fridge_energy, washing_energy],
        "Hours": [hours]*5
    })

    kmeans = KMeans(n_clusters=2)
    cluster_df["Cluster"] = kmeans.fit_predict(cluster_df)

    fig2 = px.scatter(cluster_df, x="Energy", y="Hours",
                      color=cluster_df["Cluster"].astype(str))

    st.plotly_chart(fig2, use_container_width=True)

# ---------------- CHATBOT ----------------
import streamlit as st

st.header("💬 EnergiSense AI Chatbot")

question = st.text_input("Ask a question about the project")

if question:
    q = question.lower().strip()

    if "energisense" in q:
        answer = "EnergiSense AI is an intelligent energy monitoring system that analyzes appliance electricity usage using machine learning and provides recommendations to improve energy efficiency."

    elif "purpose" in q or "goal" in q:
        answer = "The purpose of EnergiSense AI is to analyze appliance energy consumption, predict electricity usage, and help users optimize energy usage to reduce electricity bills and energy waste."

    elif "machine learning" in q or "algorithm" in q:
        answer = "EnergiSense AI uses Linear Regression to predict future electricity consumption and K-Means Clustering to group appliances based on their energy usage patterns."

    elif "predict" in q:
        answer = "The system predicts electricity consumption using the Linear Regression machine learning algorithm based on appliance usage data."

    elif "k means" in q or "clustering" in q:
        answer = "K-Means clustering is used to group appliances into categories such as high, medium, and low energy-consuming appliances."

    elif "calculate energy" in q or "formula" in q:
        answer = "Energy consumption is calculated using: Energy = Power (Watts) × Time (Hours)."

    elif "most electricity" in q:
        answer = "Air conditioners and washing machines usually consume the most electricity in households."

    elif "reduce" in q or "save" in q:
        answer = "You can reduce electricity bills by turning off unused appliances, using energy-efficient devices, and monitoring usage."

    elif "efficiency score" in q:
        answer = "Energy Efficiency Score shows how efficiently appliances use electricity."

    elif "carbon" in q:
        answer = "Carbon footprint represents CO₂ emissions due to electricity consumption."

    elif "idle" in q:
        answer = "Idle appliance detection finds devices that consume power even when not in use."

    elif "dataset" in q:
        answer = "The dataset includes appliance names, power ratings, usage hours, and energy consumption."

    elif "dashboard" in q or "visualization" in q:
        answer = "Dashboard shows charts, graphs, and energy analysis."

    else:
        answer = "Please ask a question related to EnergiSense AI."

    st.success(answer)