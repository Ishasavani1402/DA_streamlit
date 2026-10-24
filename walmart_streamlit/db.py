from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import os
import mysql.connector
load_dotenv()  # Load environment variables from .env file

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", ""),
        user=os.getenv("DB_USER", ""),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", ""),
    )



@st.cache_data(ttl=60)
def run(query: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        if cursor.description is None:      # query returned no table
            return pd.DataFrame()
        columns = [c[0] for c in cursor.description]
        rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=columns)
    finally:
        conn.close()