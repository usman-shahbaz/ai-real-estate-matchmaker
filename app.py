import json
import tempfile
import csv
import re
import streamlit as st
import pandas as pd
from phi.model.openai import OpenAIChat
from phi.agent.duckdb import DuckDbAgent
from phi.tools.pandas import PandasTools


# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Data Analysis Agent",
    page_icon="📊",
    layout="wide",
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def preprocess_and_save(file) -> tuple:
    """
    Read an uploaded CSV or Excel file, clean it, and persist it as a
    temporary CSV that DuckDB can query.

    Returns
    -------
    (temp_path, columns, dataframe)  – or (None, None, None) on error.
    """
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file, encoding="utf-8")
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file type. Please upload a .csv or .xlsx file.")
            return None, None, None

        # Escape embedded double-quotes in string columns
        for col in df.select_dtypes(include=["object"]):
            df[col] = df[col].astype(str).replace({r'"': '""'}, regex=True)

        # Parse date columns automatically
        for col in df.columns:
            if "date" in col.lower():
                df[col] = pd.to_datetime(df[col], errors="coerce")

        # Persist to a temp CSV so DuckDB can read it via file path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            temp_path = tmp.name
            df.to_csv(temp_path, index=False, quoting=csv.QUOTE_ALL)

        return temp_path, df.columns.tolist(), df

    except Exception as exc:
        st.error(f"Error processing file: {exc}")
        return None, None, None


def build_agent(api_key: str, temp_path: str) -> DuckDbAgent:
    """Instantiate a fresh DuckDbAgent pointing at the uploaded file."""
    semantic_model = {
        "tables": [
            {
                "name": "uploaded_data",
                "description": "Contains the user-uploaded dataset.",
                "path": temp_path,
            }
        ]
    }

    return DuckDbAgent(
        model=OpenAIChat(model="gpt-4o", api_key=api_key),
        semantic_model=json.dumps(semantic_model),
        tools=[PandasTools()],
        markdown=True,
        system_prompt=(
            "You are an expert data analyst. "
            "When given a question, generate the correct DuckDB SQL query "
            "to answer it, execute it, and present the results clearly. "
            "Always explain what the query does in plain English before "
            "showing the results."
        ),
    )


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("---")

    openai_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Your key is used only in this session and never stored.",
    )
    if openai_key:
        st.session_state["openai_key"] = openai_key
        st.success("API key saved for this session ✅")

    st.markdown("---")
    st.markdown(
        "**How to use**\n"
        "1. Enter your OpenAI API key above.\n"
        "2. Upload a CSV or Excel file.\n"
        "3. Ask any question about your data in plain English.\n"
        "4. Hit **Submit Query** and get instant insights!"
    )
    st.markdown("---")
    st.caption("Built with [Phidata](https://docs.phidata.com) · GPT-4o · DuckDB")


# ── Main UI ───────────────────────────────────────────────────────────────────

st.title("📊 AI Data Analysis Agent")
st.markdown(
    "Upload a dataset and ask questions in plain English – "
    "no SQL knowledge required."
)

uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx"],
    help="Supported formats: .csv, .xlsx",
)

if uploaded_file is not None:
    temp_path, columns, df = preprocess_and_save(uploaded_file)

    if df is not None:
        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader("📋 Preview")
            st.dataframe(df, use_container_width=True)

        with col2:
            st.subheader("ℹ️ Info")
            st.metric("Rows", f"{len(df):,}")
            st.metric("Columns", len(columns))
            st.markdown("**Column names**")
            for c in columns:
                st.markdown(f"- `{c}`")

        st.markdown("---")

        # ── Query interface ───────────────────────────────────────────────
        st.subheader("💬 Ask a Question")
        user_query = st.text_area(
            "Type your question here",
            placeholder=(
                "e.g. What are the top 5 products by revenue?\n"
                "     Show me average sales by region.\n"
                "     How many rows have missing values?"
            ),
            height=120,
        )

        if st.button("🚀 Submit Query", use_container_width=True):
            if not st.session_state.get("openai_key"):
                st.warning("⚠️ Please enter your OpenAI API key in the sidebar first.")
            elif not user_query.strip():
                st.warning("⚠️ Please enter a question before submitting.")
            else:
                with st.spinner("🤖 Analysing your data..."):
                    try:
                        agent = build_agent(
                            st.session_state["openai_key"], temp_path
                        )
                        response = agent.run(user_query)

                        st.subheader("📈 Results")

                        # Extract text from response content blocks
                        if hasattr(response, "content"):
                            content = response.content
                            if isinstance(content, list):
                                for block in content:
                                    if hasattr(block, "text"):
                                        st.markdown(block.text)
                            else:
                                st.markdown(str(content))
                        else:
                            st.markdown(str(response))

                    except Exception as exc:
                        st.error(f"Something went wrong: {exc}")

else:
    st.info("👆 Upload a file to get started.")
