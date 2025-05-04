import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

def draw_kLine(data: pd.DataFrame, symbol: str = ""):
    # 繪製 Plotly K 線圖
    fig = go.Figure(data=[go.Candlestick(
        x=data['time'],
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])
    title = "Candlestick chart"
    if(symbol != ""):
        title += f" of {symbol}"
    fig.update_layout(
        title=title,
        xaxis_title='Time',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )
    fig.show()

def draw_kLine_2(data: pd.DataFrame, bos_mss_data: list, symbol: str = ""):
    # kLine drawing including bos and mss data
    # 繪製 Plotly K 線圖
    fig = go.Figure(data=[go.Candlestick(
        x=data['time'],
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])
    
    # 定義不同類型的顏色和標記
    marker_colors = {
        1: 'blue',  # bos long
        2: 'orange',  # bos short
        3: 'purple',  # mss to long
        4: 'yellow'  # mss to short
    }
    
    # 繪製 bos 和 mss 標記
    for entry in bos_mss_data:
        mark_type, start_x, start_y, end_x = entry
        
        # 使用不同的顏色繪製標記
        color = marker_colors.get(mark_type, 'black')  # 默認為黑色
        
        fig.add_trace(go.Scatter(
            x=[data['time'].iloc[start_x], data['time'].iloc[end_x]],
            y=[start_y, start_y],
            mode='lines+text',
            line=dict(color=color, width=2),
            text=[f"bos" if mark_type in [1, 2] else "mss"],  # 只显示 bos 或 mss
            textposition='top center',  # Text显示在线的中间位置
            name=f"Marker {mark_type}"
        ))
    
    # 設定標題和軸標籤
    title = "Candlestick chart"
    if(symbol != ""):
        title += f" of {symbol}"
    
    fig.update_layout(
        title=title,
        xaxis_title='Time',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )
    
    # 顯示圖表
    fig.show()

def draw_rsi_div(data: pd.DataFrame, rsi_div_data: list, symbol: str = ""):
    title = "Candlestick chart"
    if(symbol != ""):
        title += f" of {symbol}"
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.1,
                    subplot_titles=(title, 'RSI'),
                    row_width=[0.2, 0.7])  # Set the height ratio
    # kLine drawing including bos and mss data
    # 繪製 Plotly K 線圖
    fig.add_trace(go.Candlestick(
        x=data['time'],
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    ), row=1, col=1)

    # Add the RSI line chart to the second row
    fig.add_trace(go.Scatter(
        x=data['time'],
        y=data['RSI'],
        mode='lines',
        name='RSI',
        line=dict(color='blue', width=2)
    ), row=2, col=1)
    
    # 定義不同類型的顏色和標記
    marker_colors = {
        1: 'green',  # bullish
        2: 'red',  # bearish
    }
    
    # 繪製 bos 和 mss 標記
    for entry in rsi_div_data:
        mark_type, start_x, start_y, end_x, end_y = entry
        
        # 使用不同的顏色繪製標記
        color = marker_colors.get(mark_type, 'black')  # 默認為黑色
        
        fig.add_trace(go.Scatter(
            x=[start_x, end_x],
            y=[start_y, end_y],
            mode='lines+text',
            line=dict(color=color, width=2),
            text=[f"bull" if mark_type in [1] else "bear"],  # 只显示 bos 或 mss
            textposition='top center',  # Text显示在线的中间位置
            name=f"Marker {mark_type}",
            showlegend=False
        ), row=2, col=1)
    
    # 設定標題和軸標籤
    title = "Candlestick chart"
    if(symbol != ""):
        title += f" of {symbol}"
    
    fig.update_layout(
        title=title,
        xaxis_title='Time',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        height=700
    )
    
    # 顯示圖表
    fig.show()

def draw_all(data: pd.DataFrame, symbol: str = ""):
    title = "Candlestick chart"
    if(symbol != ""):
        title += f" of {symbol}"
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.1,
                    subplot_titles=(title, 'RSI'),
                    row_width=[0.2, 0.7])  # Set the height ratio
    # Add the candlestick chart to the first row
    fig.add_trace(go.Candlestick(
        x=data['time'],
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    ), row=1, col=1)

    # Add the RSI line chart to the second row
    fig.add_trace(go.Scatter(
        x=data['time'],
        y=data['RSI'],
        mode='lines',
        name='RSI',
        line=dict(color='blue', width=2)
    ), row=2, col=1)
    # Add RSI=30, RSI=70 Lines into RSI chart
    fig.add_shape(
        type="line",
        xref="x2",  # 第二個x軸，也就是RSI圖的x軸
        yref="y2",  # 第二個y軸，也就是RSI圖的y軸
        x0=data['time'].min(),
        y0=30,
        x1=data['time'].max(),
        y1=30,
        line=dict(color="red", width=1, dash="dash"),
    )
    fig.add_shape(
        type="line",
        xref="x2",
        yref="y2",
        x0=data['time'].min(),
        y0=70,
        x1=data['time'].max(),
        y1=70,
        line=dict(color="green", width=1, dash="dash"),
    )

    # EMA 線
    fig.add_trace(go.Scatter(
        x=data['time'],
        y=data['EMA20'],
        mode='lines',
        line=dict(color='blue', width=1),
        name='EMA20'
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=data['time'],
        y=data['EMA40'],
        mode='lines',
        line=dict(color='orange', width=1),
        name='EMA40'
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=data['time'],
        y=data['EMA60'],
        mode='lines',
        line=dict(color='purple', width=1),
        name='EMA60'
    ), row=1, col=1)

    # Update the layout of the figure
    fig.update_layout(
        title='Candlestick and RSI Chart with EMA included',
        xaxis_title='Time',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        height=700  # Set the height of the entire figure
    )
    fig.show()
    return