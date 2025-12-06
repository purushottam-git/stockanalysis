import plotly.express as px
import numpy as np
import pandas as pd

def interactive_plot(df):
    fig = px.line(df, x='Date', y=df.columns[1:], title="Performance Comparison")
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        legend=dict(orientation="h", y=1.1)
    )
    return fig

def normalize(df):
    x = df.copy()
    for i in x.columns[1:]:
        x[i] = x[i] / x[i][0]
    return x

def daily_return(df):
    df_daily_return = df.copy()
    for i in df.columns[1:]:
        df_daily_return[i] = df[i].pct_change() * 100
        df_daily_return[i].fillna(0, inplace=True)
    return df_daily_return

def calculate_beta(stocks_daily_return, stock):
    rm = stocks_daily_return['sp500'].mean() * 252
    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[stock], 1)
    return b, a