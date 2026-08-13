import streamlit as st
import joblib
import numpy as np
import pandas as pd
import sqlite3
import plotly.express as px
import gdown
import os
import requests

# ============================================================
# 💎 DIAMOND PRO ANALYTICS DASHBOARD
# ============================================================

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Diamond Pro Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 🎨 CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #0b0f19 0%,
            #111827 50%,
            #0b1220 100%
        );
    }

    /* Main title */
    .main-title {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(
            90deg,
            #ffffff,
            #7dd3fc,
            #c084fc
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #9ca3af;
        font-size: 17px;
        margin-bottom: 25px;
    }

    /* KPI cards */
    .kpi-card {
        padding: 20px;
        border-radius: 18px;
        background: linear-gradient(
            145deg,
            rgba(30, 41, 59, 0.95),
            rgba(15, 23, 42, 0.95)
        );
        border: 1px solid rgba(148, 163, 184, 0.18);
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
        min-height: 125px;
    }

    .kpi-title {
        color: #94a3b8;
        font-size: 15px;
        font-weight: 600;
    }

    .kpi-value {
        color: #ffffff;
        font-size: 30px;
        font-weight: 800;
        margin-top: 8px;
    }

    .kpi-icon {
        font-size: 25px;
    }

    /* Insight box */
    .insight-box {
        padding: 20px;
        border-radius: 16px;
        background: linear-gradient(
            145deg,
            rgba(30, 41, 59, 0.95),
            rgba(17, 24, 39, 0.95)
        );
        border-left: 5px solid #38bdf8;
        margin: 10px 0;
    }

    .insight-title {
        font-size: 19px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 7px;
    }

    .insight-text {
        color: #cbd5e1;
        font-size: 15px;
        line-height: 1.6;
    }

    /* Segment boxes */
    .segment-box {
        padding: 18px;
        border-radius: 15px;
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(148,163,184,0.15);
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        padding: 25px;
        font-size: 14px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# 🔐 LOGIN SYSTEM
# ============================================================

users = {
    "admin": "1234",
    "winston": "raj"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:

    st.markdown(
        '<div class="main-title">💎 Diamond Pro Dashboard</div>',
        unsafe_allow_html=True
    )

    st.subheader("🔐 Secure Login")

    username = st.text_input(
        "Username",
        placeholder="Enter username"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password"
    )

    login_button = st.button(
        "🚀 Login",
        width="stretch"
    )

    if login_button:

        if username in users and users[username] == password:

            st.session_state.logged_in = True

            st.success("Login successful! Welcome to Diamond Pro Dashboard.")

            st.rerun()

        else:

            st.error("❌ Invalid username or password.")

    st.stop()


# ============================================================
# 🎬 DASHBOARD HEADER ANIMATION
# ============================================================

st.markdown("""
<div style="
text-align:center;
padding:10px;
font-size:18px;
color:#94a3b8;
">
💎 Machine Learning • Price Prediction • Market Segmentation • Business Analytics
</div>
""", unsafe_allow_html=True)


# ============================================================
# ☁️ MODEL DOWNLOAD
# ============================================================

PRICE_MODEL_ID = "1Ue0SmlssiEKBpsaGuCWQ3Ew_lTPAWgIe"

CLUSTER_MODEL_ID = "14ab3ZNiPS02XzmdHArKZKQ1njrhPTGOt"


def download_model(file_id, filename):

    if not os.path.exists(filename):

        url = (
            "https://drive.google.com/uc"
            f"?export=download&id={file_id}"
        )

        try:

            with st.spinner(f"Downloading {filename}..."):

                gdown.download(
                    url,
                    filename,
                    quiet=False
                )

        except Exception as e:

            st.error(
                f"Unable to download {filename}. "
                f"Please check the Google Drive sharing permission."
            )

            st.exception(e)

            st.stop()


download_model(
    PRICE_MODEL_ID,
    "price_model.pkl"
)

download_model(
    CLUSTER_MODEL_ID,
    "cluster_model.pkl"
)


# ============================================================
# 🤖 LOAD MACHINE LEARNING MODELS
# ============================================================

try:

    model = joblib.load(
        "price_model.pkl"
    )

    cluster = joblib.load(
        "cluster_model.pkl"
    )

except Exception as e:

    st.error(
        "❌ Unable to load the machine learning model."
    )

    st.exception(e)

    st.stop()


# ============================================================
# 💎 HEADER
# ============================================================

st.markdown(
    '<div class="main-title">💎 Diamond Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered diamond price prediction and customer market segmentation'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# 🗄️ SQLITE DATABASE
# ============================================================

conn = sqlite3.connect(
    "diamond.db",
    check_same_thread=False
)

c = conn.cursor()


c.execute("""
CREATE TABLE IF NOT EXISTS predictions (

    carat REAL,
    cut INT,
    color INT,
    clarity INT,

    x REAL,
    y REAL,
    z REAL,

    volume REAL,
    price_per_carat REAL,

    price REAL,
    cluster INT

)
""")

conn.commit()


# ============================================================
# 🎛️ SIDEBAR INPUT
# ============================================================

st.sidebar.markdown(
    "## 🔎 Diamond Input Features"
)

st.sidebar.caption(
    "Adjust the diamond characteristics to generate a prediction."
)


carat = st.sidebar.slider(
    "💎 Carat",
    min_value=0.0,
    max_value=5.0,
    value=1.0,
    step=0.01
)


x = st.sidebar.slider(
    "📏 Length (x)",
    min_value=0.0,
    max_value=10.0,
    value=5.0,
    step=0.01
)


y = st.sidebar.slider(
    "📐 Width (y)",
    min_value=0.0,
    max_value=10.0,
    value=5.0,
    step=0.01
)


z = st.sidebar.slider(
    "📏 Depth (z)",
    min_value=0.0,
    max_value=10.0,
    value=5.0,
    step=0.01
)


cut = st.sidebar.selectbox(
    "✂️ Cut",
    [0, 1, 2, 3, 4]
)


color = st.sidebar.selectbox(
    "🎨 Color",
    [0, 1, 2, 3, 4, 5, 6]
)


clarity = st.sidebar.selectbox(
    "🔍 Clarity",
    list(range(8))
)


# ============================================================
# 🧮 FEATURE ENGINEERING
# ============================================================

volume = x * y * z

price_per_carat = 0


data = np.array([
    [
        carat,
        cut,
        color,
        clarity,
        x,
        y,
        z,
        volume,
        price_per_carat
    ]
])


# ============================================================
# 📑 TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🔮 Prediction",
        "📊 Analytics",
        "💼 Business Insights",
        "📋 Data",
        "🤖 AI Assistant"
    ]
)


# ============================================================
# 🔮 TAB 1 — PRICE PREDICTION
# ============================================================

with tab1:

    st.subheader(
        "🔮 AI Diamond Price Prediction"
    )

    st.info(
        "Enter diamond characteristics in the sidebar and "
        "click Predict Price."
    )


    if st.button(
        "🚀 Predict Diamond Price",
        width="stretch"
    ):

        try:

            # Machine Learning prediction
            price = float(
                model.predict(data)[0]
            )

            # Clustering prediction
            cluster_pred = int(
                cluster.predict(data)[0]
            )


            # Cluster names
            cluster_names = {

                0: "💎 Premium",

                1: "💰 Budget",

                2: "⚖️ Mid-range"

            }


            segment = cluster_names.get(
                cluster_pred,
                "Unknown Segment"
            )


            # Save prediction
            c.execute(
                """
                INSERT INTO predictions
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    float(carat),
                    int(cut),
                    int(color),
                    int(clarity),

                    float(x),
                    float(y),
                    float(z),

                    float(volume),
                    float(price_per_carat),

                    float(price),
                    int(cluster_pred)
                )
            )

            conn.commit()


            st.success(
                "✅ Prediction generated successfully!"
            )


            # KPI cards
            col1, col2, col3 = st.columns(3)


            with col1:

                st.markdown(
                    f"""
                    <div class="kpi-card">

                    <div class="kpi-title">
                    💰 Predicted Diamond Price
                    </div>

                    <div class="kpi-value">
                    ₹ {price:,.2f}
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            with col2:

                st.markdown(
                    f"""
                    <div class="kpi-card">

                    <div class="kpi-title">
                    📊 Market Segment
                    </div>

                    <div class="kpi-value">
                    {segment}
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            with col3:

                st.markdown(
                    f"""
                    <div class="kpi-card">

                    <div class="kpi-title">
                    📦 Diamond Volume
                    </div>

                    <div class="kpi-value">
                    {volume:.2f}
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # Business recommendation for current diamond
            st.subheader(
                "💡 Recommendation"
            )


            if cluster_pred == 0:

                st.success(
                    "💎 Premium segment: suitable for "
                    "high-value customers and premium positioning."
                )

            elif cluster_pred == 1:

                st.info(
                    "💰 Budget segment: suitable for "
                    "value-focused customers and competitive pricing."
                )

            else:

                st.warning(
                    "⚖️ Mid-range segment: suitable for "
                    "customers looking for a balance between "
                    "price and quality."
                )


        except Exception as e:

            st.error(
                "Prediction failed."
            )

            st.exception(e)


# ============================================================
# 📊 LOAD DATABASE DATA
# ============================================================

df = pd.read_sql(
    "SELECT * FROM predictions",
    conn
)


# ============================================================
# 🛠️ FIX OLD SQLITE BYTE ISSUE
# ============================================================

if not df.empty:

    def fix_cluster(value):

        if isinstance(value, bytes):

            return int.from_bytes(
                value,
                byteorder="little"
            )

        try:

            return int(value)

        except:

            return 0


    df["cluster"] = df[
        "cluster"
    ].apply(fix_cluster)


    # Numeric conversion
    numeric_columns = [
        "carat",
        "cut",
        "color",
        "clarity",
        "x",
        "y",
        "z",
        "volume",
        "price_per_carat",
        "price",
        "cluster"
    ]


    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


    df = df.dropna()


# ============================================================
# 📊 TAB 2 — ANALYTICS
# ============================================================

with tab2:

    st.subheader(
        "📊 Smart Analytics Dashboard"
    )


    if df.empty:

        st.warning(
            "No prediction records available. "
            "Make at least one prediction first."
        )

    else:

        # ----------------------------------------------------
        # FILTER
        # ----------------------------------------------------

        st.markdown(
            "### 🎛️ Analytics Filters"
        )


        min_value = float(
            df["price"].min()
        )

        max_value = float(
            df["price"].max()
        )


        if min_value == max_value:

            price_range = (
                min_value,
                max_value
            )

        else:

            price_range = st.slider(
                "💰 Filter by Price",
                min_value=min_value,
                max_value=max_value,
                value=(min_value, max_value)
            )


        filtered_df = df[
            (df["price"] >= price_range[0])
            &
            (df["price"] <= price_range[1])
        ].copy()


        # ----------------------------------------------------
        # KPI
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "📦 Total Records",
                len(filtered_df)
            )


        with col2:

            st.metric(
                "💰 Average Price",
                f"₹ {filtered_df['price'].mean():,.2f}"
            )


        with col3:

            st.metric(
                "🔥 Maximum Price",
                f"₹ {filtered_df['price'].max():,.2f}"
            )


        with col4:

            st.metric(
                "📉 Minimum Price",
                f"₹ {filtered_df['price'].min():,.2f}"
            )


        st.markdown("---")


        # ----------------------------------------------------
        # CHART 1
        # ----------------------------------------------------

        colA, colB = st.columns(2)


        with colA:

            fig1 = px.line(
                filtered_df,
                y="price",
                markers=True,
                title="📈 Predicted Price Trend",
                template="plotly_dark"
            )

            st.plotly_chart(
                fig1,
                width="stretch"
            )


        # ----------------------------------------------------
        # CHART 2
        # ----------------------------------------------------

        with colB:

            chart_df = filtered_df.copy()

            chart_df["Segment"] = chart_df[
                "cluster"
            ].map({

                0: "Premium",

                1: "Budget",

                2: "Mid-range"

            })


            fig2 = px.scatter(
                chart_df,
                x="carat",
                y="price",
                color="Segment",
                size="carat",
                hover_data=[
                    "cut",
                    "color",
                    "clarity"
                ],
                title="💎 Carat vs Predicted Price",
                template="plotly_dark"
            )

            st.plotly_chart(
                fig2,
                width="stretch"
            )


        # ----------------------------------------------------
        # CLUSTER CHART
        # ----------------------------------------------------

        cluster_chart = filtered_df.copy()

        cluster_chart["Segment"] = (
            cluster_chart["cluster"]
            .map({
                0: "Premium",
                1: "Budget",
                2: "Mid-range"
            })
            .fillna("Other")
        )


        fig3 = px.histogram(
            cluster_chart,
            x="Segment",
            color="Segment",
            title="📊 Market Segment Distribution",
            template="plotly_dark"
        )


        st.plotly_chart(
            fig3,
            width="stretch"
        )


# ============================================================
# 💼 TAB 3 — BUSINESS INSIGHTS
# ============================================================

with tab3:

    st.subheader(
        "💼 Business Intelligence & Insights"
    )


    if df.empty:

        st.warning(
            "Business insights will appear after predictions are generated."
        )

    else:

        # ----------------------------------------------------
        # BUSINESS METRICS
        # ----------------------------------------------------

        total_records = len(df)

        average_price = df[
            "price"
        ].mean()

        highest_price = df[
            "price"
        ].max()

        lowest_price = df[
            "price"
        ].min()

        average_carat = df[
            "carat"
        ].mean()


        premium_count = (
            df["cluster"] == 0
        ).sum()

        budget_count = (
            df["cluster"] == 1
        ).sum()

        mid_count = (
            df["cluster"] == 2
        ).sum()


        premium_percentage = (
            premium_count / total_records
        ) * 100

        budget_percentage = (
            budget_count / total_records
        ) * 100

        mid_percentage = (
            mid_count / total_records
        ) * 100


        # ----------------------------------------------------
        # BUSINESS KPI CARDS
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)


        col1.metric(
            "💰 Avg Selling Value",
            f"₹ {average_price:,.2f}"
        )


        col2.metric(
            "💎 Avg Carat",
            f"{average_carat:.2f}"
        )


        col3.metric(
            "🏆 Premium Share",
            f"{premium_percentage:.1f}%"
        )


        col4.metric(
            "📦 Total Predictions",
            total_records
        )


        st.markdown("---")


        # ----------------------------------------------------
        # INSIGHT 1
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div class="insight-box">

            <div class="insight-title">
            💰 Pricing Insight
            </div>

            <div class="insight-text">

            The current dataset shows an average predicted
            diamond value of <b>₹ {average_price:,.2f}</b>.
            The highest predicted value is
            <b>₹ {highest_price:,.2f}</b>, while the lowest
            predicted value is <b>₹ {lowest_price:,.2f}</b>.

            Businesses can use these values to understand
            the expected price range and support pricing decisions.

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # INSIGHT 2
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div class="insight-box">

            <div class="insight-title">
            💎 Customer Segmentation Insight
            </div>

            <div class="insight-text">

            The dashboard identifies three market segments:
            <b>Premium</b>, <b>Mid-range</b> and <b>Budget</b>.

            Premium represents approximately
            <b>{premium_percentage:.1f}%</b> of predictions,
            Mid-range represents <b>{mid_percentage:.1f}%</b>,
            and Budget represents <b>{budget_percentage:.1f}%</b>.

            This segmentation can help businesses create
            different pricing and marketing strategies.

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # INSIGHT 3
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="insight-box">

            <div class="insight-title">
            🎯 Marketing Strategy
            </div>

            <div class="insight-text">

            <b>Premium customers:</b>
            Focus on high-quality diamonds, premium presentation
            and personalized service.

            <br><br>

            <b>Mid-range customers:</b>
            Focus on value-for-money combinations of quality and price.

            <br><br>

            <b>Budget customers:</b>
            Focus on competitive pricing, affordability and promotional offers.

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # INSIGHT 4
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="insight-box">

            <div class="insight-title">
            📈 Inventory Strategy
            </div>

            <div class="insight-text">

            Businesses can use the predicted price and market segment
            to prioritize inventory.

            Higher-value diamonds can be positioned for premium
            customers, while lower-value diamonds can be promoted
            through price-sensitive campaigns.

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # SEGMENT SUMMARY TABLE
        # ----------------------------------------------------

        st.markdown(
            "### 📊 Segment Business Summary"
        )


        segment_summary = (
            df.groupby("cluster")
            .agg(
                Records=("price", "count"),
                Average_Price=("price", "mean"),
                Average_Carat=("carat", "mean")
            )
            .reset_index()
        )


        segment_summary["Segment"] = (
            segment_summary["cluster"]
            .map({
                0: "💎 Premium",
                1: "💰 Budget",
                2: "⚖️ Mid-range"
            })
        )


        segment_summary["Market Share"] = (
            segment_summary["Records"]
            / total_records
            * 100
        )


        segment_summary = segment_summary[
            [
                "Segment",
                "Records",
                "Market Share",
                "Average_Price",
                "Average_Carat"
            ]
        ]


        segment_summary["Market Share"] = (
            segment_summary["Market Share"]
            .round(2)
        )


        segment_summary["Average_Price"] = (
            segment_summary["Average_Price"]
            .round(2)
        )


        segment_summary["Average_Carat"] = (
            segment_summary["Average_Carat"]
            .round(2)
        )


        st.dataframe(
            segment_summary,
            width="stretch",
            hide_index=True
        )


        # ----------------------------------------------------
        # BUSINESS RECOMMENDATION
        # ----------------------------------------------------

        st.markdown(
            "### 🚀 Recommended Business Actions"
        )


        if premium_percentage >= 40:

            st.success(
                "💎 Premium segment has strong representation. "
                "Consider increasing premium inventory and "
                "high-value customer targeting."
            )

        elif budget_percentage >= 40:

            st.info(
                "💰 Budget segment has strong representation. "
                "Consider competitive pricing, promotions and "
                "volume-based sales strategies."
            )

        else:

            st.warning(
                "⚖️ The market is relatively distributed across "
                "segments. Maintain a balanced inventory strategy."
            )


# ============================================================
# 📋 TAB 4 — DATA
# ============================================================

with tab4:

    st.subheader(
        "📋 Prediction History"
    )


    if df.empty:

        st.info(
            "No prediction data available."
        )

    else:

        display_df = df.copy()


        display_df["Segment"] = (
            display_df["cluster"]
            .map({
                0: "Premium",
                1: "Budget",
                2: "Mid-range"
            })
        )


        st.dataframe(
            display_df,
            width="stretch",
            hide_index=True
        )


        csv = df.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            "📥 Download Prediction Data",
            data=csv,
            file_name="diamond_predictions.csv",
            mime="text/csv",
            width="stretch"
        )


# ============================================================
# 🤖 TAB 5 — AI ASSISTANT
# ============================================================

with tab5:

    st.subheader(
        "🤖 Diamond AI Assistant"
    )


    st.caption(
        "Ask questions about diamond pricing, segmentation "
        "and business strategy."
    )


    user_input = st.text_input(
        "💬 Ask your question",
        placeholder="Example: Which segment should I target?"
    )


    if user_input:

        question = user_input.lower()


        # -----------------------------------------------
        # PRICE
        # -----------------------------------------------

        if "price" in question:

            if df.empty:

                st.info(
                    "💡 Generate predictions first to calculate "
                    "dashboard price insights."
                )

            else:

                st.success(
                    f"💰 Current average predicted price is "
                    f"₹ {df['price'].mean():,.2f}."
                )


        # -----------------------------------------------
        # SEGMENT
        # -----------------------------------------------

        elif (
            "segment" in question
            or "cluster" in question
        ):

            if df.empty:

                st.info(
                    "📊 No segmentation records available yet."
                )

            else:

                counts = df[
                    "cluster"
                ].value_counts()


                best_cluster = counts.idxmax()


                names = {
                    0: "💎 Premium",
                    1: "💰 Budget",
                    2: "⚖️ Mid-range"
                }


                st.success(
                    f"📊 The most represented segment is "
                    f"{names.get(best_cluster, 'Unknown')}."
                )


        # -----------------------------------------------
        # BEST DIAMOND
        # -----------------------------------------------

        elif (
            "best" in question
            or "quality" in question
        ):

            st.success(
                "💎 Diamond value is influenced by "
                "characteristics such as carat, cut, "
                "color, clarity and dimensions."
            )


        # -----------------------------------------------
        # BUSINESS
        # -----------------------------------------------

        elif (
            "business" in question
            or "strategy" in question
            or "marketing" in question
        ):

            st.info(
                "💼 Use the Business Insights tab to identify "
                "market segments, price ranges and suitable "
                "customer strategies."
            )


        # -----------------------------------------------
        # MODEL
        # -----------------------------------------------

        elif (
            "model" in question
            or "machine learning" in question
        ):

            st.success(
                "🤖 The dashboard uses trained machine learning "
                "models for diamond price prediction and "
                "market segmentation."
            )


        # -----------------------------------------------
        # DATA
        # -----------------------------------------------

        elif (
            "data" in question
            or "dataset" in question
        ):

            st.info(
                "📊 The dashboard stores prediction results "
                "in a SQLite database and uses them for "
                "analytics and business insights."
            )


        # -----------------------------------------------
        # DEFAULT
        # -----------------------------------------------

        else:

            st.info(
                "🤖 Try asking about price, model, segmentation, "
                "business strategy, marketing, quality or dataset."
            )


# ============================================================
# 🌐 LIVE API SECTION
# ============================================================

st.markdown("---")

with st.expander(
    "🌐 Optional Live API Status"
):

    st.write(
        "The application can connect to external APIs using "
        "the requests library. This section is kept separate "
        "from the diamond prediction workflow."
    )


    if st.button(
        "🔄 Test Internet Connection"
    ):

        try:

            response = requests.get(
                "https://httpbin.org/get",
                timeout=5
            )


            if response.status_code == 200:

                st.success(
                    "🌐 Internet/API connection is working."
                )

            else:

                st.warning(
                    "API returned an unexpected response."
                )


        except Exception:

            st.error(
                "Unable to connect to the external API."
            )


# ============================================================
# 🚪 LOGOUT
# ============================================================

st.sidebar.markdown("---")


if st.sidebar.button(
    "🚪 Logout",
    width="stretch"
):

    st.session_state.logged_in = False

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    💎 <b>Diamond Pro Dashboard</b><br>

    Machine Learning • Price Prediction • Market Segmentation •
    Business Intelligence<br><br>

    🚀 Winston Raj | Data Science Project

    </div>
    """,
    unsafe_allow_html=True
)
