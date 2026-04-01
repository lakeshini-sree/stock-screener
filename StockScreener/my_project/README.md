# Stock-screener-2
# 📊 AI-Powered Stock Screener & Advisory Platform

## 🔎 Overview

The **AI-Powered Stock Screener** is an intelligent backend system that allows users to analyze financial markets using **natural language queries**.

Instead of manually selecting financial filters, users can type simple queries such as:

> “Show me all stocks with PE below 5 and promoter holding above 50%.”

The system automatically:

1. Interprets the natural language query using an **LLM**
2. Converts it into a structured **DSL (Domain Specific Language)**
3. Validates the DSL rules
4. Compiles the DSL into **safe SQL queries**
5. Executes the query on the database
6. Returns filtered stock results through an API

This project demonstrates how **LLMs can be integrated with backend services to build intelligent financial analysis tools**. :contentReference[oaicite:0]{index=0}

---

# 🧠 Core Idea

Traditional stock screeners require users to manually apply filters such as:

- PE Ratio
- Revenue growth
- Debt levels
- Market capitalization

This platform allows users to simply type queries like:

> “Show technology companies with strong cash flow and low debt.”

The system then:

1️⃣ Parses the natural language input  
2️⃣ Converts it into structured screening rules  
3️⃣ Validates the rules to prevent invalid queries  
4️⃣ Executes safe database queries  
5️⃣ Returns filtered stock data

---

# 🏗️ System Architecture

The system is divided into multiple layers.

## Frontend

**Technology:** Streamlit

Responsibilities:

- Natural language query input
- Display screener results
- Interactive financial tables
- Rapid UI prototyping

---

## Backend

**Technology:** FastAPI

Responsibilities:

- REST API endpoints
- Query validation
- DSL compilation
- Business rule enforcement
- API response formatting

---

## AI Layer

**Technology:** Large Language Models (LLMs)

Responsibilities:

- Convert **Natural Language → Structured DSL JSON**
- Generate controlled output formats
- Validate schema before execution

Example output from LLM:

```json
{
  "conditions": [
    {
      "field": "revenue",
      "operator": ">",
      "value": 100000
    }
  ]
}
