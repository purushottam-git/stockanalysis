import streamlit as st
import datetime
import yfinance as yf
import pandas as pd
from pages.utils import capm_functions
import plotly.express as px

st.set_page_config(page_title="CAPM Beta", page_icon="🧩", layout="wide")

st.title('Individual Stock Beta 🧩')

col1, col2 = st.columns(2)
with col1:
    stock = st.text_input("Enter Stock Ticker (e.g. AAPL, TSLA, MSFT)", "AAPL").upper()
with col2:
    year = st.number_input("Analysis Period (Years)", 1, 10, 5)

if st.button("Analyze Stock"):
    with st.spinner(f"Fetching details and market data for {stock}..."):
        try:
            # 1. Fetch Company Details First
            ticker_obj = yf.Ticker(stock)
            
            # Using .get() is safer to avoid crashes if info is missing
            try:
                info = ticker_obj.info
            except:
                info = {}

            # --- DISPLAY COMPANY DETAILS ---
            if info:
                st.markdown("---")
                st.subheader(info.get('longName', stock))
                
                # Show Sector and Industry as little "badges"
                c1, c2, c3 = st.columns(3)
                c1.info(f"**Sector:** {info.get('sector', 'N/A')}")
                c2.info(f"**Industry:** {info.get('industry', 'N/A')}")
                c3.info(f"**Country:** {info.get('country', 'N/A')}")
                
                # Expandable Business Summary (Keeps UI clean)
                with st.expander(f"📖 Read about {info.get('shortName', stock)}"):
                    st.write(info.get('longBusinessSummary', 'No summary available.'))
                st.markdown("---")
            # -------------------------------

            # 2. Download Market Data
            end = datetime.date.today()
            start = datetime.date(end.year - year, end.month, end.day)

            # S&P 500
            SP500 = yf.download('^GSPC', start=start, end=end, progress=False)
            SP500.reset_index(inplace=True)
            SP500 = SP500[['Date', 'Close']]
            SP500.columns = ['Date', 'sp500']
            SP500['Date'] = pd.to_datetime(SP500['Date']).dt.date

            # User Stock
            stock_df = yf.download(stock, start=start, end=end, progress=False)
            
            if stock_df.empty:
                st.error(f"❌ Could not find price data for **{stock}**. Please check the ticker symbol.")
            else:
                if isinstance(stock_df.columns, pd.MultiIndex):
                    stock_df = stock_df['Close']
                else:
                    stock_df = stock_df[['Close']]
                
                stock_df.columns = [stock]
                stock_df.reset_index(inplace=True)
                stock_df['Date'] = pd.to_datetime(stock_df['Date']).dt.date

                # 3. Merge and Calculate
                df = pd.merge(stock_df, SP500, on='Date', how='inner')
                
                if len(df) < 10:
                    st.warning("Not enough overlapping data between this stock and S&P 500 to calculate Beta.")
                else:
                    daily_ret = capm_functions.daily_return(df)
                    
                    beta, alpha = capm_functions.calculate_beta(daily_ret, stock)
                    
                    # 4. Display Results
                    st.subheader("Analysis Results")
                    col_beta, col_return = st.columns(2)
                    
                    col_beta.metric("Calculated Beta", f"{beta:.2f}", 
                                    delta="High Volatility" if beta > 1.2 else "Low Volatility" if beta < 0.8 else "Market Standard",
                                    delta_color="inverse")
                    
                    # Expected Return Calculation
                    market_return = daily_ret['sp500'].mean() * 252
                    rf = 0 
                    expected_return = rf + (beta * (market_return - rf))
                    
                    col_return.metric("Expected Annual Return (CAPM)", f"{expected_return:.2f}%")
                    
                    # 5. Plot
                    fig = px.scatter(daily_ret, x='sp500', y=stock, 
                                     title=f"Regression Analysis: {stock} vs S&P 500", 
                                     template="plotly_dark",
                                     labels={'sp500': 'Market Returns (S&P 500)', stock: f'{stock} Returns'},
                                     opacity=0.6)
                    
                    # Add Regression Line
                    fig.add_scatter(x=daily_ret['sp500'], y=beta*daily_ret['sp500'] + alpha, 
                                    name='Trend Line', line=dict(color="#00e676", width=3))
                    
                    fig.update_layout(height=600, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    
                    st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")