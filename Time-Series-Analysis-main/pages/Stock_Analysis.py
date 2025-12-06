import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
from pages.utils.plotly_figure import plotly_table, close_chart, candlestick, RSI, Moving_average, MACD 

# 1. Page Config
st.set_page_config(page_title="Stock Analysis", page_icon="📊", layout="wide")

st.title("Stock Analysis Dashboard 📊")

# --- SESSION STATE INITIALIZATION ---
if 'ticker' not in st.session_state:
    st.session_state.ticker = "AAPL"

if 'timeframe' not in st.session_state:
    st.session_state.timeframe = '1y'

def update_ticker(t):
    st.session_state.ticker = t

def update_timeframe(tf):
    st.session_state.timeframe = tf

# 2. Input Section
col_input, col_date1, col_date2 = st.columns([1, 1, 1])
today = datetime.date.today()

with col_input:
    ticker = st.text_input('Stock Ticker', value=st.session_state.ticker, key='ticker_input').upper()

with col_date1:
    start_date = st.date_input("Start Date", datetime.date(today.year-1, today.month, today.day))

with col_date2:
    end_date = st.date_input("End Date", today)

# Quick Select Buttons
st.caption("🚀 **Quick Select Major Companies:**")
btn_c1, btn_c2, btn_c3, btn_c4, btn_c5 = st.columns(5)

if btn_c1.button("Apple"): update_ticker("AAPL"); st.experimental_rerun()
if btn_c2.button("Tesla"): update_ticker("TSLA"); st.experimental_rerun()
if btn_c3.button("Google"): update_ticker("GOOGL"); st.experimental_rerun()
if btn_c4.button("Microsoft"): update_ticker("MSFT"); st.experimental_rerun()
if btn_c5.button("Amazon"): update_ticker("AMZN"); st.experimental_rerun()

# 3. Fetch Data & Company Details
stock = yf.Ticker(ticker)

try:
    info = stock.info
except:
    info = {}

# --- COMPANY HEADER & DETAILS ---
st.markdown("---")

if len(info) < 2:
    st.error(f"❌ Could not find details for **{ticker}**. Please check the symbol.")
else:
    # Header
    st.subheader(f"{info.get('longName', ticker)} ({ticker})")
    
    # Sector Details
    c1, c2, c3 = st.columns(3)
    c1.info(f"**Sector:**\n{info.get('sector', 'N/A')}")
    c2.info(f"**Industry:**\n{info.get('industry', 'N/A')}")
    c3.info(f"**Country:**\n{info.get('country', 'N/A')}")

    # Summary
    with st.expander(f"📖 Read Business Summary"):
        st.write(info.get('longBusinessSummary', 'No summary available.'))

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Current Price", f"${info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))}")
    m2.metric("Market Cap", f"${info.get('marketCap', 0)/1e9:.2f}B" if info.get('marketCap') else "N/A")
    m3.metric("52 Week High", f"${info.get('fiftyTwoWeekHigh', 'N/A')}")
    m4.metric("Beta", round(info.get('beta', 0), 2) if info.get('beta') else "N/A")

    # Download Data
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)

    if data.empty:
        st.warning("No price data found for the selected date range.")
    else:
        # ==========================================
        # SECTION 1: TECHNICAL ANALYSIS
        # ==========================================
        st.markdown("---")
        st.header("1. Technical Analysis 📈")
        
        # --- TIMEFRAME BUTTONS (New Smooth Implementation) ---
        st.write("Select Timeframe:")
        tf1, tf2, tf3, tf4, tf5, tf6, tf7 = st.columns(7)
        
        if tf1.button("1M"): update_timeframe('1mo'); st.experimental_rerun()
        if tf2.button("3M"): update_timeframe('3mo'); st.experimental_rerun()
        if tf3.button("6M"): update_timeframe('6mo'); st.experimental_rerun()
        if tf4.button("YTD"): update_timeframe('ytd'); st.experimental_rerun()
        if tf5.button("1Y"): update_timeframe('1y'); st.experimental_rerun()
        if tf6.button("5Y"): update_timeframe('5y'); st.experimental_rerun()
        if tf7.button("MAX"): update_timeframe('max'); st.experimental_rerun()

        # Visual indicator of current selection
        st.caption(f"Current View: **{st.session_state.timeframe.upper()}**")

        # --- CHART SETTINGS ---
        # Placed in new columns to avoid nesting issues
        set_c1, set_c2 = st.columns(2)
        with set_c1:
            chart_type = st.selectbox('Chart Type', ['Candle', 'Line'])
        with set_c2:
            indicators = st.selectbox('Add Indicator', ['None', 'RSI', 'MACD', 'Moving Average'])

        # --- CHART RENDERING ---
        ticker_obj = yf.Ticker(ticker)
        full_history = ticker_obj.history(period='max')
        
        # Use session state timeframe
        target_period = st.session_state.timeframe

        if chart_type == 'Candle':
            fig = candlestick(full_history, target_period)
        else:
            if indicators == 'Moving Average':
                fig = Moving_average(full_history, target_period)
            else:
                fig = close_chart(full_history, target_period)

        st.plotly_chart(fig, use_container_width=True)

        if indicators == 'RSI':
            st.plotly_chart(RSI(full_history, target_period), use_container_width=True)
        elif indicators == 'MACD':
            st.plotly_chart(MACD(full_history, target_period), use_container_width=True)

        # ==========================================
        # SECTION 2: RECENT DATA
        # ==========================================
        st.markdown("---")
        st.header("2. Recent Historical Data 🗓️")
        
        c_price = data['Close'].iloc[-1]
        p_price = data['Close'].iloc[-2]
        change = c_price - p_price
        pct_change = (change / p_price) * 100
        
        st.metric(label=f"Price Change ({data.index[-1].strftime('%Y-%m-%d')})", 
                  value=f"{round(c_price, 2)}", 
                  delta=f"{round(change, 2)} ({round(pct_change, 2)}%)")

        disp_df = data.tail(10).sort_index(ascending=False).round(2)
        disp_df.index = disp_df.index.strftime('%Y-%m-%d')
        st.dataframe(disp_df)