import pandas as pd

from src.chart_generator import create_chart


def test_single_result_creates_chart():
    df = pd.DataFrame({
        "customer_name": ["A", "B", "C"],
        "revenue": [1000, 2000, 1500]
    })

    chart = create_chart(
        df,
        "Which customer generated the highest revenue?"
    )

    assert chart is not None


def test_monthly_revenue_creates_chart():
    df = pd.DataFrame({
        "month": ["Jan", "Feb", "Mar"],
        "revenue": [10000, 15000, 12000]
    })

    chart = create_chart(
        df,
        "Show me monthly revenue trend"
    )

    assert chart is not None


def test_region_distribution_creates_chart():
    df = pd.DataFrame({
        "region": ["North", "South", "East", "West"],
        "revenue": [914467, 875354, 450455, 647966]
    })

    chart = create_chart(
        df,
        "Show revenue distribution by region"
    )

    assert chart is not None


def test_product_ranking_creates_chart():
    df = pd.DataFrame({
        "product_name": [
            "Laptop Pro 14",
            "Phone X",
            "Tablet Pro",
            "Monitor",
            "Keyboard"
        ],
        "revenue": [
            544000,
            420000,
            350000,
            280000,
            190000
        ]
    })

    chart = create_chart(
        df,
        "Show the top 5 products by revenue"
    )

    assert chart is not None