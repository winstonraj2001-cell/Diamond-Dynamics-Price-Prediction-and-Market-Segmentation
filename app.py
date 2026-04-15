import streamlit as st
import joblib
import numpy as np
import pandas as pd
import sqlite3
import plotly.express as px

# ---------------- CONFIG ----------------
st.set_page_config(page_title="💎 Diamond Dashboard", layout="wide")

# ---------------- TITLE ----------------
st.title("💎 Diamond Analytics Dashboard")

# ---------------- LOAD MODELS ----------------
model = joblib.load('price_model.pkl')
cluster = joblib.load('cluster_model.pkl')

# ---------------- DATABASE ----------------
conn = sqlite3.connect('diamond.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS predictions (
carat REAL, cut INT, color INT, clarity INT,
x REAL, y REAL, z REAL,
volume REAL, price_per_carat REAL,
price REAL, cluster INT)
''')
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

data = np.array([[carat,cut,color,clarity,x,y,z,volume,price_per_carat]])

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["🔮 Prediction", "📊 Analytics", "📋 Data"])

# ---------------- PREDICTION ----------------
with tab1:
    if st.button("🚀 Predict Price"):

        price = float(model.predict(data)[0])
        cluster_pred = int(cluster.predict(data)[0])

        c.execute("INSERT INTO predictions VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                  (float(carat), int(cut), int(color), int(clarity),
                   float(x), float(y), float(z),
                   float(volume), float(price_per_carat),
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

# 🔥 FIX OLD BYTE DATA (VERY IMPORTANT)
if not df.empty:
    df['cluster'] = df['cluster'].apply(
        lambda x: int.from_bytes(x, 'little') if isinstance(x, bytes) else int(x)
    )

    df = df.astype({
        'carat': float,
        'cut': int,
        'color': int,
        'clarity': int,
        'x': float,
        'y': float,
        'z': float,
        'volume': float,
        'price_per_carat': float,
        'price': float,
        'cluster': int
    })

# ---------------- ANALYTICS ----------------
with tab2:
    if df.empty:
        st.warning("No data yet. Make predictions first.")
    else:
        st.subheader("📊 Dashboard Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", len(df))
        col2.metric("Avg Price", f"₹ {df.price.mean():,.2f}")
        col3.metric("Max Price", f"₹ {df.price.max():,.2f}")

        colA, colB = st.columns(2)

        with colA:
            fig1 = px.line(df, y="price", title="📈 Price Trend", template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)

        with colB:
            fig2 = px.scatter(df, x="carat", y="price",
                              color=df["cluster"].astype(str),
                              title="💎 Carat vs Price",
                              template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.histogram(df, x=df["cluster"].astype(str),
                            title="📊 Cluster Distribution",
                            template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)

# ---------------- DATA ----------------
with tab3:
    if df.empty:
        st.info("No data available.")
    else:
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button("📥 Download CSV", csv, "diamond_data.csv", "text/csv")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🚀 Winston Raj | Diamond ML Dashboard")