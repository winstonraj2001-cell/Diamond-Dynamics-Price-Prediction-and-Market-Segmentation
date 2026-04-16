import streamlit as st
import joblib
import numpy as np
import pandas as pd
import sqlite3
import plotly.express as px
import gdown
import os
import requests

# ---------------- CONFIG ----------------
st.set_page_config(page_title="💎 Diamond Pro Dashboard", layout="wide")

# ---------------- LOGIN ----------------
users = {"admin": "1234", "winston": "raj"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid Credentials ❌")

    st.stop()

# ---------------- ANIMATION ----------------
st.markdown("""
<style>
@keyframes fadeIn {
    0% {opacity: 0;}
    100% {opacity: 1;}
}
.block-container {
    animation: fadeIn 1s ease-in;
}
button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ---------------- DOWNLOAD MODELS ----------------
PRICE_MODEL_ID = "1Ue0SmlssiEKBpsaGuCWQ3Ew_lTPAWgIe"
CLUSTER_MODEL_ID = "14ab3ZNiPS02XzmdHArKZKQ1njrhPTGOt"

if not os.path.exists("price_model.pkl"):
    gdown.download(f"https://drive.google.com/uc?export=download&id={PRICE_MODEL_ID}",
                   "price_model.pkl", quiet=False)

if not os.path.exists("cluster_model.pkl"):
    gdown.download(f"https://drive.google.com/uc?export=download&id={CLUSTER_MODEL_ID}",
                   "cluster_model.pkl", quiet=False)

# ---------------- LOAD MODELS ----------------
model = joblib.load("price_model.pkl")
cluster = joblib.load("cluster_model.pkl")

# ---------------- TITLE ----------------
st.title("💎 Diamond Analytics Dashboard")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("diamond.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS predictions (
carat REAL, cut INT, color INT, clarity INT,
x REAL, y REAL, z REAL,
volume REAL, price_per_carat REAL,
price REAL, cluster INT)
""")
conn.commit()

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔎 Input Features")

carat = st.sidebar.slider("Carat", 0.0, 5.0, 1.0)
x = st.sidebar.slider("Length (x)", 0.0, 10.0, 5.0)
y = st.sidebar.slider("Width (y)", 0.0, 10.0, 5.0)
z = st.sidebar.slider("Depth (z)", 0.0, 10.0, 5.0)

cut = st.sidebar.selectbox("Cut", [0,1,2,3,4])
color = st.sidebar.selectbox("Color", [0,1,2,3,4,5,6])
clarity = st.sidebar.selectbox("Clarity", list(range(8)))

# ---------------- FEATURES ----------------
volume = x * y * z
price_per_carat = 0

data = np.array([[carat, cut, color, clarity, x, y, z, volume, price_per_carat]])

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs(["🔮 Prediction", "📊 Analytics", "📋 Data", "🤖 AI Assistant"])

# ---------------- PREDICTION ----------------
with tab1:
    if st.button("🚀 Predict Price"):

        price = float(model.predict(data)[0])
        cluster_pred = int(cluster.predict(data)[0])

        c.execute("INSERT INTO predictions VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                  (carat, cut, color, clarity,
                   x, y, z,
                   volume, price_per_carat,
                   price, cluster_pred))
        conn.commit()

        cluster_names = {
            0: "💎 Premium",
            1: "💰 Budget",
            2: "⚖️ Mid-range"
        }

        col1, col2 = st.columns(2)
        col1.metric("💰 Price", f"₹ {price:,.2f}")
        col2.metric("📊 Segment", cluster_names.get(cluster_pred))

# ---------------- LOAD DATA ----------------
df = pd.read_sql("SELECT * FROM predictions", conn)

# FIX BYTE ISSUE
if not df.empty:
    df["cluster"] = df["cluster"].apply(
        lambda x: int.from_bytes(x, "little") if isinstance(x, bytes) else int(x)
    )

# ---------------- ANALYTICS ----------------
with tab2:

    if df.empty:
        st.warning("No data yet.")
    else:
        st.subheader("📊 Dashboard Overview")

        # FILTER
        min_price = st.slider("Filter Price", 0, int(df.price.max()), (0, int(df.price.max())))
        df = df[(df.price >= min_price[0]) & (df.price <= min_price[1])]

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", len(df))
        col2.metric("Avg Price", f"₹ {df.price.mean():,.2f}")
        col3.metric("Max Price", f"₹ {df.price.max():,.2f}")

        colA, colB = st.columns(2)

        fig1 = px.line(df, y="price", title="📈 Price Trend", template="plotly_dark")
        colA.plotly_chart(fig1, use_container_width=True)

        fig2 = px.scatter(df, x="carat", y="price",
                          color=df["cluster"].astype(str),
                          title="💎 Carat vs Price",
                          template="plotly_dark")
        colB.plotly_chart(fig2, use_container_width=True)

        fig3 = px.histogram(df, x=df["cluster"].astype(str),
                            title="📊 Cluster Distribution",
                            template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)

        # LIVE API
        st.subheader("🌍 Live Market Insight")
        try:
            res = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
            btc = res.json()
            st.success(f"💰 Bitcoin Price: ${btc['bpi']['USD']['rate']}")
        except:
            st.warning("API not available")

# ---------------- DATA ----------------
with tab3:
    if df.empty:
        st.info("No data available.")
    else:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", csv, "diamond_data.csv")

# ---------------- AI CHATBOT ----------------
with tab4:
    st.subheader("🤖 AI Assistant")

    user_input = st.text_input("Ask something about diamonds or price")

    if user_input:
        if "price" in user_input.lower():
            st.success("💡 Price depends on carat, clarity, and cut quality.")
        elif "best" in user_input.lower():
            st.success("💎 Best diamonds are high clarity + ideal cut.")
        else:
            st.info("🤖 I'm learning... Try asking about price or quality!")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🚀 Winston Raj | Diamond Pro Dashboard")
