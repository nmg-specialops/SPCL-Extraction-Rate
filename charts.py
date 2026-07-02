import plotly.graph_objects as go
import pandas as pd


# --------------------------------------------------------
# EXTRACTION RATE CHART
# --------------------------------------------------------

def extraction_rate_chart(df):

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df["Date"],

            y=df["Extraction Rate"] * 100,

            mode="lines+markers",

            name="Extraction Rate",

            line=dict(
                color="#0B6E4F",
                width=3
            ),

            marker=dict(
                size=6
            ),

            hovertemplate=
                "<b>%{x|%Y-%m-%d}</b><br>"
                "Extraction Rate: %{y:.2f}%<extra></extra>"

        )

    )

    fig.update_layout(

        title="Historical Extraction Rate",

        xaxis_title="Date",

        yaxis_title="Extraction Rate (%)",

        template="plotly_white",

        hovermode="x unified",

        height=550,

        margin=dict(
            l=30,
            r=30,
            t=60,
            b=30
        )

    )

    fig.update_yaxes(
        ticksuffix="%"
    )

    return fig


# --------------------------------------------------------
# MOVING AVERAGE
# --------------------------------------------------------

def moving_average_chart(df, window):

    data = df.copy()

    data["Moving Average"] = (

        data["Extraction Rate"]

        .rolling(window)

        .mean()

        * 100

    )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=data["Date"],

            y=data["Extraction Rate"] * 100,

            mode="lines",

            name="Extraction Rate",

            line=dict(
                color="lightgray",
                width=2
            )

        )

    )

    fig.add_trace(

        go.Scatter(

            x=data["Date"],

            y=data["Moving Average"],

            mode="lines",

            name=f"{window}-Period Moving Average",

            line=dict(
                color="#1F77B4",
                width=4
            )

        )

    )

    fig.update_layout(

        title="Extraction Rate Moving Average",

        xaxis_title="Date",

        yaxis_title="Extraction Rate (%)",

        template="plotly_white",

        hovermode="x unified",

        height=550

    )

    fig.update_yaxes(
        ticksuffix="%"
    )

    return fig
