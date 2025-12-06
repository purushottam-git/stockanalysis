import plotly.graph_objects as go
import dateutil.relativedelta
import pandas_ta_classic as pta # USING THE CORRECT IMPORT
import datetime
import pandas as pd

# --- COMMON CHART STYLE ---
def apply_dark_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        grid=dict(rows=1, columns=1),
        margin=dict(l=20, r=20, t=30, b=20),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='#333')
    return fig

def plotly_table(dataframe):
    # Dark themed table
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>"+str(i)+"<b>" for i in dataframe.columns],
            line_color='#333', fill_color='#00e676',
            align='center', font=dict(color='black', size=14), height=35,
        ),
        cells=dict(
            values=[dataframe[i] for i in dataframe.columns], 
            fill_color='#1e1e1e',
            align='left', line_color='#333', font=dict(color="white", size=13), height=30
        ))
    ])
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)')
    return fig

def filter_data(dataframe, num_period):
    # TIMEZONE FIX
    if dataframe.index.tz is not None:
        dataframe.index = dataframe.index.tz_localize(None)
        
    if num_period == '1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
    elif num_period == '5d':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
    elif num_period == '6mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
    elif num_period == '1y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
    elif num_period == '5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
    elif num_period == 'ytd':
        date = datetime.datetime(dataframe.index[-1].year, 1, 1)
    else:
        date = dataframe.index[0]
    
    df_reset = dataframe.reset_index()
    return df_reset[df_reset['Date'] > date]

def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'], 
                             mode='lines', name='Close', 
                             line=dict(width=2, color='#00e676'), fill='tozeroy', fillcolor='rgba(0, 230, 118, 0.1)'))
    
    fig = apply_dark_theme(fig)
    fig.update_layout(height=500)
    return fig

def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=dataframe['Date'],
                    open=dataframe['Open'], high=dataframe['High'],
                    low=dataframe['Low'], close=dataframe['Close'],
                    increasing_line_color='#00e676', decreasing_line_color='#ff1744'))

    fig = apply_dark_theme(fig)
    fig.update_layout(showlegend=False, height=500)
    return fig

def RSI(dataframe, num_period):
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe, num_period)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe.RSI, name='RSI', line=dict(width=2, color='#ff9100')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[70]*len(dataframe), name='Overbought', line=dict(color='#ff1744', dash='dash')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[30]*len(dataframe), name='Oversold', line=dict(color='#00e676', dash='dash')))

    fig = apply_dark_theme(fig)
    fig.update_layout(yaxis_range=[0, 100], height=250)
    return fig

def Moving_average(dataframe, num_period):
    dataframe['SMA_50'] = pta.sma(dataframe['Close'], 50)
    dataframe = filter_data(dataframe, num_period)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'], mode='lines', name='Close', line=dict(color='#00e676')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'], mode='lines', name='SMA 50', line=dict(color='#d500f9', width=2)))
    
    fig = apply_dark_theme(fig)
    fig.update_layout(height=500)
    return fig

def MACD(dataframe, num_period):
    macd = pta.macd(dataframe['Close'])
    dataframe['MACD'] = macd.iloc[:, 0]
    dataframe['MACD Signal'] = macd.iloc[:, 1]
    dataframe['MACD Hist'] = macd.iloc[:, 2]
    dataframe = filter_data(dataframe, num_period)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=dataframe['Date'], y=dataframe['MACD Hist'], name='Hist', marker_color='#2979ff'))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MACD'], name='MACD', line=dict(color='#ff9100')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MACD Signal'], name='Signal', line=dict(color='#00e676')))
    
    fig = apply_dark_theme(fig)
    fig.update_layout(height=250)
    return fig

def Moving_average_forecast(forecast):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast.index[:-30], y=forecast['Close'].iloc[:-30], mode='lines', name='Historical', line=dict(color='#888')))
    fig.add_trace(go.Scatter(x=forecast.index[-31:], y=forecast['Close'].iloc[-31:], mode='lines', name='Forecast', line=dict(color='#00e676', width=3)))
    
    fig = apply_dark_theme(fig)
    fig.update_layout(height=500)
    return fig