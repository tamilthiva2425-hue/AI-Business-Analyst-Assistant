import os
from dotenv import load_dotenv
from google import genai

from llm import generate_sql
from database import execute_sql
from chart_generator import create_chart

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.5-flash-lite"


def is_safe_sql(sql):

    sql_clean = sql.strip().lower()

    if not (
        sql_clean.startswith("select")
        or sql_clean.startswith("with")
    ):
        return False

    blocked_keywords = [
        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "truncate ",
        "create ",
        "grant ",
        "revoke ",
    ]

    for keyword in blocked_keywords:
        if keyword in sql_clean:
            return False

    return True


def generate_business_insight(question, sql, result):

    result_text = result.to_string(index=False)

    prompt = f"""
You are a professional Business Analyst.

Business question:
{question}

SQL query:
{sql}

SQL result:
{result_text}

Give a concise business analysis with:

1. Direct Answer
2. Key Business Insight
3. Business Recommendation

Use ONLY the supplied result.
Do not invent numbers.
Keep it professional and useful for a business manager.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text.strip()


def run_business_question(question):

    print("\nGenerating SQL with AI...")

    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print("-" * 50)
    print(sql)

    print("\nChecking SQL safety...")

    if not is_safe_sql(sql):
        raise ValueError("Unsafe SQL query detected.")

    print("SQL safety check: PASSED")

    print("\nExecuting SQL in MySQL...")

    result = execute_sql(sql)

    print("\nBusiness Result:")
    print("-" * 50)
    print(result.to_string(index=False))

    print("\nGenerating Chart...")

    chart = create_chart(result, question)

    if chart is not None:
        chart.write_html("data/ai_generated_chart.html")

        print(
            "\nChart created successfully:"
            "\ndata/ai_generated_chart.html"
        )
    else:
        print("\nNo suitable chart could be generated.")

    print("\nGenerating Business Insight...")

    insight = generate_business_insight(
        question,
        sql,
        result
    )

    print("\nAI Business Insight:")
    print("-" * 50)
    print(insight)


if __name__ == "__main__":

    question = input(
        "Enter your business question: "
    )

    try:

        run_business_question(question)

    except Exception as error:

        print("\nERROR:")
        print(error)