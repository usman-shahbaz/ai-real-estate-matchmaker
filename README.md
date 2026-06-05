# 📊 AI Data Analysis Agent

A conversational data analysis tool that lets you query CSV and Excel files using plain English. Powered by **GPT-4o**, **Phidata**, and **DuckDB** no SQL knowledge required.

---

## ✨ Features

- **Natural Language Queries** — Ask questions like *"What are the top 5 products by revenue?"* and get instant answers
- **File Upload Support** — Works with `.csv` and `.xlsx` files
- **Auto Schema Detection** — Automatically infers column types and parses dates
- **DuckDB Backend** — Fast in-process SQL execution on your data
- **Streamlit UI** — Clean, interactive browser interface

---

## 🗂️ Project Structure

```
ai-data-analysis-agent/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Files to exclude from Git
├── sample_data/
│   └── sales_sample.csv    # Example dataset to try the app
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/ai-data-analysis-agent.git
cd ai-data-analysis-agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your OpenAI API key

Copy the example env file and fill in your key:

```bash
cp .env.example .env
```

Open `.env` and add your key:

```
OPENAI_API_KEY=sk-...
```

> You can also enter the key directly in the app's sidebar at runtime — no `.env` file needed.

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧪 Try It with Sample Data

A sample sales dataset is included in `sample_data/sales_sample.csv`. Upload it in the app and try questions like:

- *"What is the total revenue per region?"*
- *"Which product had the highest sales in Q4?"*
- *"Show me monthly sales trends."*
- *"How many orders were placed by each customer?"*

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Phidata](https://docs.phidata.com) | AI agent framework |
| [GPT-4o](https://platform.openai.com) | Language model (natural language → SQL) |
| [DuckDB](https://duckdb.org) | In-process SQL engine |
| [Streamlit](https://streamlit.io) | Web UI |
| [Pandas](https://pandas.pydata.org) | Data loading & preprocessing |
