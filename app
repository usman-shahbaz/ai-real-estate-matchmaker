import json
import tempfile
import csv
import streamlit as s
import pandas as pd
from phi.model.openai import OpenAIChat

def preprocess_and_save(file):
    try:
        # Handle different file types
        if file.name.endswith('.csv'):
            df = pd.read_csv(file, encoding='utf-8')
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
            
        # Clean and format data
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str).replace({r'"': '""'}, regex=True)
    
