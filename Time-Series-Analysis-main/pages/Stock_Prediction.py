import streamlit as st
from pages.utils.model_train import get_data, get_rolling_mean, get_differencing_order, scaling, evaluate_model, get_forecast, inverse_scaling
import pandas as pd
import yfinance as yf
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast

st.set_page_config(
        page_title="Stock Prediction",
        page_icon="chart_with_downwards_trend",
        layout="wide",
    )

st.title("Stock Prediction")

col1, col2, col3 = st.columns(3)

with col1:
    # ADDED .upper() HERE -> Automatically converts input to Uppercase
    ticker = st.text_input('Stock Ticker', 'AAPL').upper()

# --- Display Company Details ---
try:
    if ticker:
        stock = yf.Ticker(ticker)
        # Use .info to get details, handle potential errors gracefully
        info = stock.info
        
        # Only show if we found valid data
        if info and len(info) > 5:
            st.markdown(f"### {info.get('longName', ticker)}")
            st.write(f"**Sector:** {info.get('sector', 'N/A')} | **Industry:** {info.get('industry', 'N/A')}")
            
            with st.expander("Read Business Summary"):
                st.write(info.get('longBusinessSummary', 'No summary available.'))
            st.markdown("---")
except Exception:
    pass
# -------------------------------

rmse = 0

st.subheader('Predicting Next 30 days Close Price for: '+ticker)

close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)
rmse = evaluate_model(scaled_data, differencing_order)

st.write("**Model RMSE Score:**",rmse)

forecast = get_forecast(scaled_data, differencing_order)

forecast['Close'] = inverse_scaling( scaler, forecast['Close'])
st.write('##### Forecast Data (Next 30 days)')
fig_tail = plotly_table(forecast.sort_index(ascending = True).round(3))
fig_tail.update_layout(height = 220)
st.plotly_chart(fig_tail, use_container_width=True)

forecast = pd.concat([rolling_price, forecast])

st.plotly_chart(Moving_average_forecast(forecast.iloc[150:]), use_container_width=True)