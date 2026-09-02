import plotly.express as px
import pandas as pd


def create_chart(df, question):

    if df is None or df.empty:
        return None

    question_lower = question.lower()
    columns = df.columns.tolist()

    # ---------------------------------------------------------
    # CLEAN COLUMN NAMES
    # ---------------------------------------------------------

    df = df.copy()

    # Try to identify date column
    date_column = None

    for column in columns:

        if any(word in column.lower() for word in [
            "date",
            "month",
            "year",
            "time"
        ]):

            try:
                df[column] = pd.to_datetime(
                    df[column]
                )

                date_column = column
                break

            except Exception:
                pass


    # ---------------------------------------------------------
    # IDENTIFY NUMERIC COLUMN
    # ---------------------------------------------------------

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    # Remove obvious ID columns
    numeric_columns = [
        col for col in numeric_columns
        if "id" not in col.lower()
    ]


    # ---------------------------------------------------------
    # DATE / TREND QUESTIONS
    # ---------------------------------------------------------

    trend_words = [
        "trend",
        "over time",
        "monthly",
        "month",
        "yearly",
        "year",
        "daily",
        "daily trend",
        "growth"
    ]

    is_trend_question = any(
        word in question_lower
        for word in trend_words
    )

    if (
        is_trend_question
        and date_column is not None
        and numeric_columns
    ):

        y_column = numeric_columns[0]

        df = df.sort_values(
            date_column
        )

        fig = px.line(
            df,
            x=date_column,
            y=y_column,
            markers=True,
            title=question
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title=date_column.replace(
                "_", " "
            ).title(),
            yaxis_title=y_column.replace(
                "_", " "
            ).title(),
            hovermode="x unified"
        )

        return fig


    # ---------------------------------------------------------
    # PIE / SHARE QUESTIONS
    # ---------------------------------------------------------

    pie_words = [
        "share",
        "percentage",
        "percent",
        "distribution",
        "proportion",
        "breakdown"
    ]

    is_pie_question = any(
        word in question_lower
        for word in pie_words
    )

    if (
        is_pie_question
        and len(columns) >= 2
    ):

        category = columns[0]

        value_candidates = [
            col for col in columns[1:]
            if pd.api.types.is_numeric_dtype(
                df[col]
            )
        ]

        if value_candidates:

            value = value_candidates[0]

            fig = px.pie(
                df,
                names=category,
                values=value,
                title=question,
                hole=0.35
            )

            fig.update_layout(
                template="plotly_white"
            )

            return fig


    # ---------------------------------------------------------
    # BAR CHART
    # ---------------------------------------------------------

    if len(columns) >= 2:

        category_column = columns[0]

        # Find numeric metric
        metric_candidates = [
            col for col in columns[1:]
            if pd.api.types.is_numeric_dtype(
                df[col]
            )
        ]

        if metric_candidates:

            metric_column = metric_candidates[0]

        elif numeric_columns:

            metric_column = numeric_columns[0]

        else:

            metric_column = columns[1]


        # Sort descending for business comparisons
        if pd.api.types.is_numeric_dtype(
            df[metric_column]
        ):

            df = df.sort_values(
                metric_column,
                ascending=False
            )


        fig = px.bar(
            df,
            x=category_column,
            y=metric_column,
            title=question,
            text_auto=True
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title=category_column.replace(
                "_", " "
            ).title(),
            yaxis_title=metric_column.replace(
                "_", " "
            ).title(),
            hovermode="x unified"
        )

        return fig


    # ---------------------------------------------------------
    # SINGLE NUMERIC RESULT
    # ---------------------------------------------------------

    if len(columns) == 1:

        column = columns[0]

        if pd.api.types.is_numeric_dtype(
            df[column]
        ):

            fig = px.bar(
                df,
                y=column,
                title=question,
                text_auto=True
            )

            fig.update_layout(
                template="plotly_white",
                yaxis_title=column.replace(
                    "_", " "
                ).title()
            )

            return fig


    return None