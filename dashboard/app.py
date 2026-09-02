import os
import sys
import re
import warnings

import streamlit as st


# =========================================================
# WARNING
# =========================================================

warnings.filterwarnings(
    "ignore",
    message="pandas only supports SQLAlchemy"
)


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

SRC_PATH = os.path.join(
    PROJECT_ROOT,
    "src"
)

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


# =========================================================
# PROJECT IMPORTS
# =========================================================

from llm import generate_sql
from database import execute_sql
from chart_generator import create_chart


# =========================================================
# GEMINI
# =========================================================

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY is missing from .env")
    st.stop()

client = genai.Client(
    api_key=GEMINI_API_KEY
)

MODEL = "gemini-3.5-flash-lite"


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="AI Business Analyst",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1400px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    .title {
        font-size: 42px;
        font-weight: 750;
        letter-spacing: -1px;
    }

    .subtitle {
        font-size: 17px;
        color: #667085;
        margin-bottom: 30px;
    }

    .insight-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e4e7ec;
        background: #ffffff;
        margin-bottom: 15px;
    }

    .insight-heading {
        font-size: 19px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .insight-content {
        font-size: 16px;
        line-height: 1.6;
        color: #344054;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SQL SAFETY
# =========================================================

def is_safe_sql(sql):

    if not sql or not sql.strip():
        return False

    cleaned_sql = sql.strip().rstrip(";").strip()

    # Only SELECT / WITH queries
    if not re.match(r"^(SELECT|WITH)\b", cleaned_sql, re.IGNORECASE):
        return False

    # Block write / destructive operations
    blocked = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "RENAME",
        "GRANT",
        "REVOKE",
        "EXEC",
        "EXECUTE"
    ]

    for keyword in blocked:
        if re.search(
            rf"\b{keyword}\b",
            cleaned_sql,
            re.IGNORECASE
        ):
            return False

    # Prevent multiple SQL statements
    if ";" in cleaned_sql:
        return False

    # Prevent SQL comments
    if "--" in cleaned_sql:
        return False

    if "/*" in cleaned_sql or "*/" in cleaned_sql:
        return False

    return True


# =========================================================
# CLEAN GEMINI RESPONSE
# =========================================================

def clean_text(text):

    if not text:
        return ""

    # Remove HTML tags
    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    # Remove markdown
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("```", "")
    text = text.replace("*", "")
    text = text.replace("#", "")

    # Fix broken spacing
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# GET BUSINESS INSIGHT
# =========================================================

def generate_business_insight(
    question,
    sql,
    result
):

    result_text = result.to_string(
        index=False
    )

    prompt = f"""
You are a senior Business Analyst.

Business Question:
{question}

SQL Query:
{sql}

Query Result:
{result_text}

Return exactly this format:

DIRECT ANSWER:
Your direct answer here.

KEY BUSINESS INSIGHT:
Your key business finding here.

BUSINESS RECOMMENDATION:
Your recommendation here.

Rules:
- Plain text only.
- Never generate HTML.
- Never generate Markdown.
- Never use asterisks.
- Never use hashtags.
- Never use underscores.
- Never use bullet points.
- Do not invent numbers.
- Use only the query result.
- Keep each section concise.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return clean_text(
        response.text
    )


# =========================================================
# PARSE INSIGHT
# =========================================================

def parse_insight(text):

    text = clean_text(text)

    direct = ""
    key_insight = ""
    recommendation = ""

    # DIRECT ANSWER
    match = re.search(
        r"DIRECT ANSWER\s*:?\s*(.*?)(?=KEY BUSINESS INSIGHT|BUSINESS RECOMMENDATION|$)",
        text,
        re.IGNORECASE
    )

    if match:
        direct = match.group(1).strip()

    # KEY BUSINESS INSIGHT
    match = re.search(
        r"KEY BUSINESS INSIGHT\s*:?\s*(.*?)(?=BUSINESS RECOMMENDATION|$)",
        text,
        re.IGNORECASE
    )

    if match:
        key_insight = match.group(1).strip()

    # BUSINESS RECOMMENDATION
    match = re.search(
        r"BUSINESS RECOMMENDATION\s*:?\s*(.*)",
        text,
        re.IGNORECASE
    )

    if match:
        recommendation = match.group(1).strip()

    return (
        direct,
        key_insight,
        recommendation
    )


# =========================================================
# INSIGHT DISPLAY
# =========================================================

def display_insight(
    number,
    title,
    text
):

    if not text:
        return

    st.markdown(
        f"### {number}. {title}"
    )

    st.write(text)

    st.divider()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="title">🤖 AI Business Analyst</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Transform natural-language business questions into '
    'data-driven answers, visualizations and recommendations.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Configuration")

st.sidebar.subheader(
    "Database Connection"
)

mysql_password = st.sidebar.text_input(
    "MySQL Password",
    type="password"
)

st.sidebar.divider()

st.sidebar.write(
    "Host: localhost"
)

st.sidebar.write(
    "Database: business_analytics"
)

st.sidebar.write(
    "User: root"
)

st.sidebar.divider()

st.sidebar.caption(
    "Python • MySQL • Gemini • Plotly"
)


# =========================================================
# QUESTION
# =========================================================

st.subheader(
    "Ask your business question"
)

question = st.text_area(
    "Business Question",
    placeholder=(
        "Example: Which region generated "
        "the highest revenue?"
    ),
    height=110,
    label_visibility="collapsed"
)

analyze = st.button(
    "🚀 Analyze Business Question",
    type="primary"
)


# =========================================================
# RUN ANALYSIS
# =========================================================

if analyze:

    if not question.strip():

        st.warning(
            "Please enter a business question."
        )

        st.stop()


    if not mysql_password:

        st.warning(
            "Please enter your MySQL password "
            "in the sidebar."
        )

        st.stop()


    try:

        # =================================================
        # 1. SQL GENERATION
        # =================================================

        with st.spinner(
            "🤖 Understanding your business question..."
        ):

            sql = generate_sql(
                question
            )


        st.subheader(
            "🧠 AI-Generated SQL"
        )

        st.code(
            sql,
            language="sql"
        )


        # =================================================
        # 2. SQL SAFETY
        # =================================================

        if not is_safe_sql(sql):

            st.error(
                "Unsafe SQL query detected. "
                "The query was blocked."
            )

            st.stop()


        st.success(
            "✓ SQL safety validation passed"
        )


        # =================================================
        # 3. MYSQL
        # =================================================

        with st.spinner(
            "🗄️ Querying business database..."
        ):

            result = execute_sql(
                sql,
                mysql_password
            )


        # =================================================
        # 4. RESULT
        # =================================================

        st.subheader(
            "📊 Query Result"
        )

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )


        # =================================================
        # 5. CHART
        # =================================================

        with st.spinner(
            "📈 Building visualization..."
        ):

            chart = create_chart(
                result,
                question
            )


        if chart is not None:

            st.subheader(
                "📈 Visualization"
            )

            st.plotly_chart(
                chart,
                use_container_width=True
            )


        # =================================================
        # 6. AI ANALYSIS
        # =================================================

        with st.spinner(
            "💡 Generating business analysis..."
        ):

            raw_insight = (
                generate_business_insight(
                    question,
                    sql,
                    result
                )
            )


        direct, key_insight, recommendation = (
            parse_insight(
                raw_insight
            )
        )


        # =================================================
        # 7. DISPLAY INSIGHTS
        # =================================================

        st.subheader(
            "💡 AI Business Analysis"
        )

        display_insight(
            1,
            "Direct Answer",
            direct
        )

        display_insight(
            2,
            "Key Business Insight",
            key_insight
        )

        display_insight(
            3,
            "Business Recommendation",
            recommendation
        )


        # =================================================
        # FOOTER
        # =================================================

        st.caption(
            "AI Business Analyst • "
            "Natural Language → SQL → MySQL → "
            "Visualization → Business Insight"
        )


    except Exception as error:

        st.error(
            f"Something went wrong:\n\n{error}"
        )