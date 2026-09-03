import os
import pandas as pd
import plotly.express as px


def detect_chart_type(df, question):
    """
    Automatically chooses the most suitable visualization
    based on the business question and query result.
    """

    question = question.lower().strip()

    # Single result → KPI-style bar chart
    if len(df) == 1:
        return "bar"

    # Time-based questions → line chart
    time_words = [
        "monthly",
        "month",
        "daily",
        "day",
        "weekly",
        "week",
        "yearly",
        "year",
        "trend",
        "over time",
        "growth"
    ]

    if any(word in question for word in time_words):
        return "line"

    # Distribution / share questions → donut
    distribution_words = [
        "distribution",
        "percentage",
        "percent",
        "share",
        "proportion",
        "breakdown"
    ]

    if any(word in question for word in distribution_words):
        return "donut"

    # Ranking questions → bar
    ranking_words = [
        "top",
        "bottom",
        "highest",
        "lowest",
        "best",
        "worst",
        "rank"
    ]

    if any(word in question for word in ranking_words):
        return "bar"

    # Find categorical and numeric columns
    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        exclude=["number"]
    ).columns.tolist()

    # Two useful columns → bar
    if len(categorical_columns) >= 1 and len(numeric_columns) >= 1:
        return "bar"

    return "table"


def create_chart(df, question):
    """
    Create an automatic business visualization.
    """

    if df is None or df.empty:
        return None

    chart_type = detect_chart_type(df, question)

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        exclude=["number"]
    ).columns.tolist()

    # ---------------------------------------------------------
    # BAR CHART
    # ---------------------------------------------------------

    if chart_type == "bar":

        if categorical_columns and numeric_columns:

            x_column = categorical_columns[0]
            y_column = numeric_columns[0]

            fig = px.bar(
                df,
                x=x_column,
                y=y_column,
                title=question,
                text=y_column
            )

            fig.update_traces(
                texttemplate="%{text:,.0f}",
                textposition="inside"
            )

            fig.update_layout(
                template="plotly_white",
                height=500,
                xaxis_title=x_column.replace("_", " ").title(),
                yaxis_title=y_column.replace("_", " ").title(),
                title_x=0
            )

            return fig

    # ---------------------------------------------------------
    # LINE CHART
    # ---------------------------------------------------------

    if chart_type == "line":

        if categorical_columns and numeric_columns:

            x_column = categorical_columns[0]
            y_column = numeric_columns[0]

            fig = px.line(
                df,
                x=x_column,
                y=y_column,
                title=question,
                markers=True
            )

            fig.update_layout(
                template="plotly_white",
                height=500,
                xaxis_title=x_column.replace("_", " ").title(),
                yaxis_title=y_column.replace("_", " ").title(),
                title_x=0
            )

            return fig

    # ---------------------------------------------------------
    # DONUT CHART
    # ---------------------------------------------------------

    if chart_type == "donut":

        if categorical_columns and numeric_columns:

            label_column = categorical_columns[0]
            value_column = numeric_columns[0]

            fig = px.pie(
                df,
                names=label_column,
                values=value_column,
                hole=0.55,
                title=question
            )

            fig.update_layout(
                template="plotly_white",
                height=500,
                title_x=0
            )

            return fig

    # ---------------------------------------------------------
    # FALLBACK TABLE
    # ---------------------------------------------------------

    return None