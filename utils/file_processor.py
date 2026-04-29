"""
utils/file_processor.py
Handles ingestion, cleaning, and temp-file creation for uploaded data files.
"""

import csv
import tempfile
from typing import Optional, Tuple, List

import pandas as pd
import streamlit as st


def preprocess_and_save(
    file,
) -> Tuple[Optional[str], Optional[List[str]], Optional[pd.DataFrame]]:
    """
    Read a CSV or Excel upload, apply basic cleaning, and persist to a
    temp CSV file that DuckDB can read.

    Parameters
    ----------
    file : UploadedFile
        Streamlit UploadedFile object.

    Returns
    -------
    temp_path : str | None
        Absolute path to the temp CSV file.
    columns : list[str] | None
        Column names after cleaning.
    df : pd.DataFrame | None
        In-memory DataFrame for preview.
    """
    try:
        # ── 1. Read file ──────────────────────────────────────────────────────
        if file.name.endswith(".csv"):
            df = pd.read_csv(file, encoding="utf-8", on_bad_lines="skip")
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file type. Please upload a CSV or XLSX file.")
            return None, None, None

        # ── 2. Strip whitespace from column names ─────────────────────────────
        df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]

        # ── 3. Sanitise string columns (escape internal double-quotes) ────────
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str).str.replace('"', '""', regex=False)

        # ── 4. Parse date-like columns ────────────────────────────────────────
        for col in df.columns:
            if "date" in col or "time" in col:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        # ── 5. Drop fully-empty rows ──────────────────────────────────────────
        df.dropna(how="all", inplace=True)
        df.reset_index(drop=True, inplace=True)

        # ── 6. Write to temp CSV ──────────────────────────────────────────────
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".csv", mode="w", newline="", encoding="utf-8"
        ) as tmp:
            df.to_csv(tmp, index=False, quoting=csv.QUOTE_ALL)
            temp_path = tmp.name

        return temp_path, df.columns.tolist(), df

    except Exception as exc:
        st.error(f"Error processing file: {exc}")
        return None, None, None
