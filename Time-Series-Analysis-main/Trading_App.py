import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Trading Guide App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for "White Theme" & Professional Styling
st.markdown("""
    <style>
    /* Force White Background and Black Text */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Header Styling */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        color: #0E1117;
        font-weight: 700;
    }
    h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        color: #31333F;
    }
    
    /* Custom Card Styling for Sections */
    .css-1r6slb0 {
        background-color: #F0F2F6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #FF2B2B;
        color: white;
    }
    
    /* Divider Styling */
    hr {
        border-top: 2px solid #F0F2F6;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Hero Section (Split into 2 columns)
hero_col1, hero_col2 = st.columns([1, 1.5])

with hero_col1:
    st.image("https://img.freepik.com/free-vector/gradient-stock-market-concept_23-2149166910.jpg", use_column_width=True)

with hero_col2:
    st.title("Master the Markets 🚀")
    st.markdown("""
    ### Your All-In-One Financial Companion
    
    Welcome to the **Trading Guide App**, a professional dashboard designed to bridge the gap between complex financial data and actionable insights. 
    
    Whether you are a day trader looking for technical indicators or a long-term investor analyzing fundamental health, this platform provides the tools you need.
    
    **👈 Select a module from the Sidebar to start analyzing.**
    """)
    
    # --- NO NESTED COLUMNS HERE ---
    st.markdown("---")
    st.caption("**Data Source:** Yahoo Finance (Live) | **Powered By:** Plotly & Streamlit")

st.markdown("---")

# 4. Detailed Features Section
st.header("🛠️ Comprehensive Tools Available")

# Row 1 (Split into 2 columns)
feat_col1, feat_col2 = st.columns(2)

with feat_col1:
    st.subheader("1. Deep Stock Analysis 📊")
    st.markdown("""
    **Understand the heartbeat of any company.**
    
    *   **Fundamental Data:** Access critical metrics like P/E Ratio, Market Cap, EPS, and Sector performance instantly.
    *   **Technical Indicators:** Visualize market trends using Moving Averages (SMA), RSI (Relative Strength Index), and MACD.
    *   **Interactive Charts:** Zoom into specific timeframes (1M, YTD, 5Y) with high-performance Candle and Line charts.
    """)

with feat_col2:
    st.subheader("2. AI-Powered Prediction 🔮")
    st.markdown("""
    **Peek into the future with Machine Learning.**
    
    *   **ARIMA Modeling:** We utilize the *AutoRegressive Integrated Moving Average* model to forecast stock prices.
    *   **30-Day Forecast:** Get a generated trend line for the next 30 days based on historical volatility and momentum.
    *   **RMSE Evaluation:** We transparently show the Root Mean Square Error so you know how accurate the model is.
    """)

st.markdown("---")

# Row 2 (Split into 2 columns)
feat_col3, feat_col4 = st.columns(2)

with feat_col3:
    st.subheader("3. CAPM Return Analysis 📉")
    st.markdown("""
    **Evaluate Risk vs. Reward.**
    
    *   **Portfolio Theory:** Based on the Capital Asset Pricing Model (CAPM), we calculate the expected return of an asset.
    *   **Market Comparison:** Compare your chosen stocks against the S&P 500 benchmark.
    *   **Normalized Growth:** See how \$1 invested in different stocks would have grown over time compared to each other.
    """)

with feat_col4:
    st.subheader("4. Beta & Volatility Calculator 🧩")
    st.markdown("""
    **Measure Market Sensitivity.**
    
    *   **Beta Calculation:** Determine if a stock is more volatile (Beta > 1) or stable (Beta < 1) compared to the overall market.
    *   **Regression Analysis:** Visualize the relationship between a stock's daily returns and the market's returns using scatter plots.
    *   **Strategic Planning:** Use Beta values to hedge your portfolio or take on calculated risks.
    """)

st.markdown("---")

# 5. Footer
st.markdown("""
<div style="text-align: center; color: #888;">
    <p>Built with ❤️ using Python & Streamlit | Data provided for educational purposes.</p>
</div>
""", unsafe_allow_html=True)