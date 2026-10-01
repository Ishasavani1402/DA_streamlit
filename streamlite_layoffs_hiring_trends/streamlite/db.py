import os
import pandas as pd
import streamlit as st
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool

CSV = Path(__file__).parent.parent / "datasets" / "clean_dataset.csv"

@st.cache_resource
def get_engine():
    if os.environ.get("DB_HOST"):          # your laptop: real MySQL
        url = (f"mysql+mysqlconnector://{os.environ['DB_USER']}:"
               f"{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}/{os.environ['DB_NAME']}")
        return create_engine(url, pool_pre_ping=True)
    eng = create_engine("sqlite://", poolclass=StaticPool,   # cloud: runs from CSV
                        connect_args={"check_same_thread": False})
    pd.read_csv(CSV).to_sql("clean_dataset", eng, index=False)
    return eng

@st.cache_data(ttl=3600)
def run(query: str) -> pd.DataFrame:
    with get_engine().connect() as conn:
        return pd.read_sql_query(text(query), conn)