import streamlit as st
import datetime
import pandas as pd
import yfinance as yf
from pages.utils import capm_functions
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Config
st.set_page_config(page_title="CAPM Return", page_icon="📉", layout="wide")

st.title('CAPM: Expected Returns & Portfolio Analysis 📉')

# 2. Input Section (Hybrid: Dropdown + Text Input)
st.markdown("### 1. Select Assets")
col1, col2 = st.columns([2, 1])

with col1:
    # Default list
    default_tickers = ['TSLA', 'AAPL', 'NFLX', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'META']
    selected_stocks = st.multiselect("Select from Popular Stocks", default_tickers, ['TSLA', 'AAPL', 'MSFT'])
    
    # Custom Input
    custom_stocks_input = st.text_input("➕ Add Custom Stocks (comma separated, e.g. KO, JPM, BTC-USD)")
    
    # Combine the lists
    if custom_stocks_input:
        custom_list = [x.strip().upper() for x in custom_stocks_input.split(',') if x.strip()]
        stocks_list = list(set(selected_stocks + custom_list))
    else:
        stocks_list = selected_stocks

with col2:
    year = st.number_input("Analysis Period (Years)", 1, 15, 3)
    st.caption("Recommended: 3-5 Years for stable Beta calculation.")

# 3. Calculation Engine
if st.button("🚀 Calculate CAPM Return", help="Run the Capital Asset Pricing Model"):
    if not stocks_list:
        st.error("Please select at least one stock.")
    else:
        with st.spinner("Downloading Market Data & Calculating Beta..."):
            try:
                end = datetime.date.today()
                start = datetime.date(end.year - year, end.month, end.day)

                # --- A. Download Market Data (S&P 500) ---
                SP500 = yf.download('^GSPC', start=start, end=end, progress=False)
                SP500.reset_index(inplace=True)
                SP500 = SP500[['Date', 'Close']]
                SP500.columns = ['Date', 'sp500']
                SP500['Date'] = pd.to_datetime(SP500['Date']).dt.date

                # --- B. Download Stock Data Loop ---
                stocks_df = pd.DataFrame()
                valid_stocks = []

                for stock in stocks_list:
                    data = yf.download(stock, start=start, end=end, progress=False)
                    
                    if not data.empty:
                        if isinstance(data.columns, pd.MultiIndex):
                            data = data['Close']
                        else:
                            data = data[['Close']]
                        
                        data.columns = [stock]
                        
                        if stocks_df.empty:
                            stocks_df = data
                        else:
                            stocks_df = stocks_df.join(data, how='outer')
                        valid_stocks.append(stock)
                
                if stocks_df.empty:
                    st.error("No valid data found for the selected stocks.")
                    st.stop()

                stocks_df.reset_index(inplace=True)
                stocks_df['Date'] = pd.to_datetime(stocks_df['Date']).dt.date
                
                # --- C. Merge Stocks with Market ---
                merged_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

                # --- D. Visuals: Performance Chart ---
                st.markdown("---")
                st.subheader("2. Historical Price Performance (Normalized)")
                st.caption("This chart shows how $1 invested in each asset would have grown over the selected period.")
                
                normalized_df = capm_functions.normalize(merged_df)
                
                # Custom Plotly Chart for better visuals
                fig_perf = px.line(normalized_df, x='Date', y=normalized_df.columns[1:], 
                                   template="plotly_dark", height=500)
                fig_perf.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                                       legend=dict(orientation="h", y=1.1))
                st.plotly_chart(fig_perf, use_container_width=True)

                # --- E. Calculations ---
                daily_ret = capm_functions.daily_return(merged_df)
                
                beta = {}
                for i in valid_stocks:
                    b, a = capm_functions.calculate_beta(daily_ret, i)
                    beta[i] = b

                # CAPM Inputs
                rm = daily_ret['sp500'].mean() * 252 # Annualized Market Return
                rf = 0 # Risk Free Rate (Simplified to 0, or set to 4.0 for 4%)
                
                # Create Results DataFrame
                results_data = []
                for stock, b_val in beta.items():
                    exp_ret = rf + (b_val * (rm - rf))
                    results_data.append({
                        "Stock": stock,
                        "Beta": round(b_val, 2),
                        "Expected Return (%)": round(exp_ret, 2),
                        "Volatility": "High" if b_val > 1 else "Low"
                    })
                
                res_df = pd.DataFrame(results_data)

                # --- F. Detailed Results Section ---
                st.markdown("---")
                st.subheader("3. CAPM Analysis Results")
                
                # Display Key Metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("Market Return (Annualized)", f"{round(rm, 2)}%", "S&P 500 Performance")
                m2.metric("Risk Free Rate", f"{rf}%", "Assumed Baseline")
                m3.metric("Assets Analyzed", len(valid_stocks))

                # Split layout for Table and Charts
                c1, c2 = st.columns([1, 1])

                with c1:
                    st.markdown("#### 📋 Calculated Values")
                    # Using standard dataframe (removed use_container_width for compatibility)
                    st.dataframe(res_df.style.background_gradient(subset=['Expected Return (%)'], cmap='Greens'))
                    
                    st.info("""
                    **How to interpret:**
                    *   **Beta > 1:** The stock moves *more* than the market (Aggressive).
                    *   **Beta < 1:** The stock moves *less* than the market (Defensive).
                    *   **Expected Return:** The theoretical return you should expect for taking this amount of risk.
                    """)

                with c2:
                    st.markdown("#### 📊 Expected Return Comparison")
                    fig_bar = px.bar(res_df, x='Stock', y='Expected Return (%)', color='Beta',
                                     template="plotly_dark", text_auto=True,
                                     color_continuous_scale='Bluered')
                    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
                    st.plotly_chart(fig_bar, use_container_width=True)

                # --- G. Risk vs Reward Scatter ---
                st.markdown("#### ⚖️ Risk vs. Reward Landscape")
                fig_scatter = px.scatter(res_df, x='Beta', y='Expected Return (%)', 
                                         color='Stock', size='Expected Return (%)',
                                         text='Stock', template="plotly_dark",
                                         title="Higher Beta should yield Higher Returns (CAPM Theory)")
                
                # Add a reference line for Market
                fig_scatter.add_vline(x=1, line_dash="dash", line_color="green", annotation_text="Market Risk (Beta=1)")
                fig_scatter.update_traces(textposition='top center')
                fig_scatter.update_layout(height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_scatter, use_container_width=True)

            except Exception as e:
                st.error(f"Analysis Failed: {e}")