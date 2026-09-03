# AI Business Analyst Assistant

An AI-powered business analytics application that allows users to ask business questions in natural language and receive SQL queries, database results, visualizations, and business insights.

## 📌 Project Overview

Business users often depend on analysts for repetitive data queries and reporting tasks.

This project demonstrates an AI-assisted business analytics workflow where a user can ask a question in natural language, Gemini generates the required SQL query, the query is validated for safety, data is retrieved from MySQL, an appropriate visualization is generated automatically, and business insights are produced from the results.

The project also includes Power BI dashboards built using the same business data for interactive business reporting and analysis.

## 🎯 Business Problem

Business teams frequently need answers to questions such as:

- Which region generated the highest revenue?
- Which product generated the highest revenue?
- Which customer generated the highest revenue?
- What is the monthly revenue trend?
- How is revenue distributed across regions?
- Which products are performing best?

Answering these questions manually can require repeated SQL queries, data preparation, analysis, and report creation.

The AI Business Analyst Assistant streamlines this analytical workflow.

## 💡 Solution

The AI analyst application follows this workflow:

**Natural Language Business Question**

↓

**Gemini AI**

↓

**SQL Query Generation**

↓

**SQL Safety Validation**

↓

**MySQL Database**

↓

**Query Result**

↓

**Automatic Visualization using Plotly**

↓

**AI Business Analysis**

↓

**Business Recommendation**

Power BI is used separately as the business intelligence and dashboarding layer using the same business data.

## 🚀 Key Features

### 1. Natural Language Business Queries

Users can ask business questions using normal language instead of writing SQL manually.

Example:

> Which region generated the highest revenue?

### 2. AI-Powered SQL Generation

Gemini converts the user's natural-language business question into a SQL query based on the available business data.

The application understands the project database structure and generates queries for business analysis.

### 3. SQL Safety Validation

Before executing an AI-generated query, the application performs SQL safety validation.

Only read-oriented queries beginning with:

- `SELECT`
- `WITH`

are allowed.

The application blocks operations such as:

- `INSERT`
- `UPDATE`
- `DELETE`
- `DROP`
- `ALTER`
- `TRUNCATE`
- `CREATE`
- `RENAME`
- `GRANT`
- `REVOKE`
- `EXEC`
- `EXECUTE`

It also blocks:

- Multiple SQL statements
- SQL comments

This provides a basic safety layer before executing AI-generated SQL against the database.

### 4. MySQL Data Retrieval

Validated queries are executed against the MySQL database:

`business_analytics`

The application retrieves the required business data and displays the query results to the user.

### 5. Automatic Visualization

The application automatically selects a suitable chart based on the business question and query result.

The current visualization engine supports:

- Bar charts
- Line charts
- Donut charts
- Ranking visualizations
- Table fallback when a chart is not appropriate

Examples:

- Revenue ranking → Bar chart
- Monthly revenue trend → Line chart
- Revenue distribution by region → Donut chart
- Top products by revenue → Bar chart

### 6. AI Business Analysis

After retrieving the data, Gemini generates business-oriented analysis consisting of:

1. Direct Answer
2. Key Business Insight
3. Business Recommendation

This moves the application beyond simply displaying numbers and helps translate analytical results into business meaning

### 7. Power BI Dashboards

The project also contains Power BI dashboards for interactive business reporting.

The Power BI implementation contains three completed pages:

#### Sales Performance Dashboard

Includes:

- Transactions
- Units Sold
- Revenue
- Average Transaction Value
- Monthly Target vs Actual Sales
- Regional Target vs Actual Sales
- Monthly Revenue Trend
- Revenue by Region
- Region filtering
- Month filtering

#### Customer Analysis

Provides customer-level business analysis.

#### Product Analysis

Provides product-level performance analysis.

Power BI and the AI analyst application use the same business data source, but they serve different purposes:

**AI Analyst**

Natural Language → Gemini → SQL → MySQL → Plotly → Business Insight

**Power BI**

Business Data → Power BI → Interactive Dashboards

## 🛠️ Technology Stack

| Technology | Usage |
|---|---|
| Python | Application development, ETL and analytics |
| SQL | Data querying and analysis |
| MySQL | Business database |
| Gemini API | SQL generation and business insight generation |
| Streamlit | Interactive AI analyst application |
| Plotly | Automatic interactive visualizations |
| Power BI | Business intelligence dashboards |
| Pandas | Data cleaning and processing |
| NumPy | Data processing |
| Pytest | Automated testing |

## 🗄️ Database

The project uses a MySQL database named:

`business_analytics`

### Main Tables

#### `customers`

Contains customer information:

- `customer_id`
- `customer_name`
- `email`
- `city`
- `region`
- `customer_segment`
- `registration_date`

#### `products`

Contains product information:

- `product_id`
- `product_name`
- `category`
- `sub_category`
- `unit_cost`
- `selling_price`

#### `sales`

Contains transaction-level sales information.

#### `sales_targets`

Contains sales target information by region and date.

#### `sales_cleaned`

Contains cleaned and validated sales data used by the analytics workflow.

### Important Relationships

```text
sales_cleaned.product_id → products.product_id

sales_cleaned.customer_id → customers.customer_id
🔄 Data Preparation & ETL

The project includes an ETL process for preparing the sales data before analysis.

ETL Workflow
Raw Sales Data
      ↓
Data Cleaning
      ↓
Data Validation
      ↓
Duplicate Removal
      ↓
Missing Value Handling
      ↓
Processed CSV
      ↓
MySQL sales_cleaned Table

The processed dataset currently contains:

94 clean records
0 duplicate records
0 missing values

The cleaned data is stored in:

data/processed/sales_cleaned.csv
🤖 AI Analyst Application

The Streamlit application provides an end-to-end natural-language analytics workflow.

Example

User asks:

Which product generated the highest revenue?

The application performs the following steps:

Understands the business question.
Generates SQL using Gemini.
Displays the generated SQL.
Validates the SQL for safety.
Executes the query against MySQL.
Displays the query result.
Automatically generates a suitable visualization.
Analyzes the result using Gemini.
Produces a business recommendation.
📈 Example Business Questions

The application has been tested with questions such as:

Which region generated the highest revenue?
Which product generated the highest revenue?
Which customer generated the highest revenue?
Show me monthly revenue trend
Show revenue distribution by region
Show the top 5 products by revenue
Example Results

The application successfully identified:

Highest revenue region → North
Highest revenue product → Laptop Pro 14
Highest revenue customer → Shalini Gupta

It also successfully generated:

Monthly revenue trend visualization
Regional revenue distribution visualization
Top 5 product revenue ranking visualization
🧪 Testing

The project includes automated tests using Pytest.

The current chart-generation test suite covers:

Single-result visualization
Monthly revenue trend
Regional revenue distribution
Product ranking

Current test result:

4 passed

Run the tests with:

python -m pytest tests/test_chart_generator.py -v
📁 Project Structure
AI - bussines analyst/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── processed/
│   │   └── sales_cleaned.csv
│   └── ...
│
├── database/
│   └── schema.sql
│
├── sql/
│   └── analysis_queries.sql
│
├── src/
│   ├── ai_business_analyst.py
│   ├── chart_generator.py
│   ├── database.py
│   ├── etl.py
│   └── llm.py
│
├── tests/
│   └── test_chart_generator.py
│
├── requirements.txt
├── README.md
└── .env
⚙️ How to Run
1. Clone the repository
git clone <your-github-repository-url>
cd "AI - bussines analyst"
2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment

Windows:

venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Configure Gemini API

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key

Do not commit the .env file or expose your API key.

6. Configure MySQL

Create the required database and tables using:

database/schema.sql

The application expects the MySQL database:

business_analytics
7. Run the Streamlit application
python -m streamlit run dashboard/app.py

The application will open in the browser.

🔐 Security

The application includes basic SQL safety validation before executing AI-generated queries.

The safety layer:

Allows read-only SELECT and WITH queries
Blocks data modification operations
Blocks destructive database operations
Blocks multiple SQL statements
Blocks SQL comments

API keys and database credentials should be stored in environment variables and never committed to GitHub.

🏗️ Project Architecture
AI Analyst Workflow
                    Business User
                         │
                         │
                  Natural Language
                         │
                         ▼
                  ┌─────────────┐
                  │  Gemini AI  │
                  └──────┬──────┘
                         │
                    SQL Query
                         │
                         ▼
               ┌──────────────────┐
               │ SQL Safety Check │
               └────────┬─────────┘
                        │
                   Safe SQL
                        │
                        ▼
                ┌──────────────┐
                │    MySQL     │
                │ business_    │
                │  analytics   │
                └──────┬───────┘
                       │
                 Query Result
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
        ┌──────────┐      ┌────────────┐
        │  Plotly  │      │  Gemini AI │
        │  Charts  │      │  Analysis  │
        └──────────┘      └────────────┘
Power BI Workflow
              Business Data
                   │
                   ▼
              ┌─────────┐
              │  MySQL  │
              └────┬────┘
                   │
                   ▼
             ┌───────────┐
             │ Power BI  │
             └─────┬─────┘
                   │
                   ▼
          Interactive Dashboards
🎓 Skills Demonstrated

This project demonstrates practical skills in:

Business analysis
SQL querying
MySQL
Data cleaning
ETL
Python
Pandas
NumPy
Data visualization
Plotly
Power BI
Dashboard development
Natural-language-to-SQL
Generative AI
AI-assisted analytics
Business insight generation
SQL safety validation
Automated testing
📌 Project Outcome

This project combines AI-assisted analytics with traditional business intelligence.

It demonstrates an end-to-end analytical workflow:

Business Question
       ↓
Data Retrieval
       ↓
Analysis
       ↓
Visualization
       ↓
Business Insight
       ↓
Recommendation

The AI analyst reduces the need for users to manually write SQL for common business questions while the Power BI dashboards provide interactive business reporting.

👨‍💻 Author

Tamilselvan A

Data Analytics | Python | SQL | MySQL | Power BI | AI Analytics