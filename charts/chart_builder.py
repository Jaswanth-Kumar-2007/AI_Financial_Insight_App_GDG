import plotly.graph_objects as go


def create_line_chart(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['Close'],
            mode='lines',
            name='Close Price'
        )
    )

    fig.update_layout(
        template='plotly_dark',
        height=500
    )

    return fig


def create_candlestick_chart(df):

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']
            )
        ]
    )

    fig.update_layout(
        template='plotly_dark',
        height=600
    )

    return fig