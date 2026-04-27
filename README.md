# AI Data Analysis Agent

> Upload a CSV or Excel file, ask questions in plain English, and get instant SQL-powered insights — no SQL expertise required.

Built with **GPT-4o**, **Phidata**, **DuckDB**, and **Streamlit**, following the [Unwind AI tutorial](https://www.theunwindai.com/p/build-an-ai-data-analysis-agent).

---

## ✨ Features

| Feature | Description |
|---|---|
| 📤 File Upload | CSV and Excel (.xlsx) support with automatic schema detection |
| 💬 Natural Language | Ask questions in plain English — the agent writes SQL for you |
| ⚡ DuckDB Engine | Fast, in-process analytical SQL queries |
| 📜 Query History | Every question and answer saved in the session |
| 🎨 Dark-themed UI | Clean Streamlit interface with custom theming |
| 🧪 Unit Tests | Pytest suite covering file processing logic |

---

## 🗂️ Project Structure

```
ai-data-analysis-agent/
│
├── app/
│   └── ai_data_analyst.py      # Main Streamlit application
│
├── utils/
│   ├── __init__.py
│   ├── file_processor.py       # File ingestion & cleaning logic
│   └── ui_helpers.py           # Reusable Streamlit UI components
│
├── assets/
│   └── sample_data.csv         # Sample dataset for quick testing
│
├── tests/
│   ├── __init__.py
│   └── test_file_processor.py  # Pytest unit tests
│
├── .streamlit/
│   └── config.toml             # Streamlit theme & server settings
│
├── .env.example                # Environment variable template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1 · Clone the repository

```bash
git clone https://github.com/<your-username>/ai-data-analysis-agent.git
cd ai-data-analysis-agent
```

### 2 · Create and activate a virtual environment

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3 · Install dependencies

```bash
pip install -r requirements.txt
```

### 4 · Configure your API key

```bash
cp .env.example .env
# Open .env and set OPENAI_API_KEY=sk-...
```

> You can also enter the key directly in the app sidebar — no `.env` file needed.

### 5 · Run the app

```bash
streamlit run app/ai_data_analyst.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 💡 Example Queries

Once you've uploaded a file, try questions like:

- *"Show me the first 10 rows"*
- *"What is the total revenue by region?"*
- *"Which product category has the highest average unit price?"*
- *"How many orders were placed each month?"*
- *"Which columns have missing values and how many?"*

---

## 🛠️ Tech Stack

| Library | Version | Purpose |
|---|---|---|
| [Streamlit](https://streamlit.io) | ≥ 1.32 | Web UI |
| [Phidata](https://docs.phidata.com) | ≥ 2.4 | Agent framework |
| [OpenAI](https://platform.openai.com) | ≥ 1.30 | GPT-4o language model |
| [DuckDB](https://duckdb.org) | ≥ 0.10 | In-process SQL engine |
| [Pandas](https://pandas.pydata.org) | ≥ 2.0 | Data preprocessing |

---

## 🔮 Potential Enhancements

- [ ] Support for more file formats (JSON, Parquet, Google Sheets)
- [ ] Automatic chart generation from query results
- [ ] Export analysis results to PDF / Excel
- [ ] Multi-file join queries
- [ ] Persistent query history across sessions

---

## 📄 License

MIT — feel free to use and extend this project.

---

## 🙏 Acknowledgements

Tutorial by [Unwind AI](https://www.theunwindai.com/p/build-an-ai-data-analysis-agent) · Agent framework by [Phidata](https://docs.phidata.com)
