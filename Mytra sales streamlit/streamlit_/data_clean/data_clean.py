"""Data cleaning pipeline for Myntra Sales Analysis """

import io
import numpy as np
import pandas as pd
import streamlit as st

def upload_file():
    """Show uploader. Returns (DataFrame, file_name) or (None, None)."""
    st.subheader("Upload Sales Data")
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload your sales dataset.",
    )
    if uploaded_file is None:
        return None, None
 
    st.success(f"Uploaded: {uploaded_file.name}")
    return pd.read_csv(uploaded_file), uploaded_file.name
 
 
def show_raw_preview(raw_df: pd.DataFrame) -> None:
    st.subheader("Raw Data Preview")
    st.caption(f"{raw_df.shape[0]} rows × {raw_df.shape[1]} columns")
    st.dataframe(raw_df)
 
 
def show_report(clean_df: pd.DataFrame, report: dict) -> None:
    before = report["before"]
 
    st.subheader("Cleaning Report")
 
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", report["final_shape"][0])
    c2.metric("Columns", report["final_shape"][1])
    c3.metric("Duplicates found", before["duplicates"])
 
    with st.expander("1. Standardized column names"):
        st.write(report["columns"])
 
    with st.expander("2. Null check (before filling)"):
        st.dataframe(before["nulls"])
 
    with st.expander("3. Nulls after handling (rating → median)"):
        st.dataframe(report["nulls_after_fill"])
 
    with st.expander("4. Unique values in categorical columns"):
        st.dataframe(report["unique_values"])
 
    if "crosstab" in report:
        with st.expander("5. Category vs Size crosstab"):
            st.dataframe(report["crosstab"])
 
    with st.expander("6. Whitespace check"):
        if report["whitespace_left"]:
            st.warning(f"Whitespace still exists in: {report['whitespace_left']}")
        else:
            st.success("No leading/trailing whitespace left.")
 
    st.subheader("Clean Data Preview")
    st.dataframe(clean_df.head(20))
 
    st.download_button(
        label="⬇️ Download Clean Data (CSV)",
        data=clean_df.to_csv(index=False).encode("utf-8"),
        file_name="clean_dataset.csv",
        mime="text/csv",
    )

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Replace 'NaN' strings with real NaN, and make column names snake_case."""
    df = df.replace("NaN", np.nan)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def drop_columns(df: pd.DataFrame, cols=("customer_name",)) -> pd.DataFrame:
    """Drop unneeded columns (only if they exist)."""
    return df.drop(columns=[c for c in cols if c in df.columns])


def quality_report(df: pd.DataFrame) -> dict:
    """Null check, duplicate count and shape."""
    info_buf = io.StringIO()
    df.info(buf=info_buf)
    return {
        "info": info_buf.getvalue(),
        "nulls": df.isnull().sum().rename("null_count").to_frame(),
        "duplicates": int(df.duplicated().sum()),
        "shape": df.shape,
    }


def fill_numeric_nulls(df: pd.DataFrame, num_cols=("rating",)) -> pd.DataFrame:
    """Fill nulls in numeric columns with the median."""
    for col in num_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
    return df


def unique_values(df: pd.DataFrame) -> pd.DataFrame:
    """Unique values of every categorical (object) column."""
    rows = []
    for col in df.select_dtypes(include="object").columns:
        vals = df[col].dropna().unique()
        rows.append({
            "column": col,
            "unique_count": len(vals),
            "values": ", ".join(sorted(map(str, vals))[:30])
                      + (" ..." if len(vals) > 30 else ""),
        })
    return pd.DataFrame(rows)


def strip_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """Remove leading/trailing spaces from all text columns."""
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df


def whitespace_remaining(df: pd.DataFrame) -> list:
    """Return columns that still have leading/trailing spaces (should be empty)."""
    bad = []
    for col in df.select_dtypes(include="object").columns:
        s = df[col].astype("string")
        if s.str.startswith(" ", na=False).any() or s.str.endswith(" ", na=False).any():
            bad.append(col)
    return bad


def clean_data(raw_df: pd.DataFrame):
    """Run the full pipeline. Returns (clean_df, report dict)."""
    report = {}
    df = raw_df.copy()

    df = standardize_columns(df)
    report["columns"] = list(df.columns)

    df = drop_columns(df)

    report["before"] = quality_report(df)

    df = fill_numeric_nulls(df)
    report["nulls_after_fill"] = df.isnull().sum().rename("null_count").to_frame()

    report["unique_values"] = unique_values(df)
    if {"category", "size"}.issubset(df.columns):
        report["crosstab"] = pd.crosstab(df["category"], df["size"])

    df = strip_whitespace(df)
    report["whitespace_left"] = whitespace_remaining(df)

    report["final_shape"] = df.shape
    return df, report


def render_data_cleaning() -> None:
    """Render the complete Data Cleaning page."""
    raw_df, file_name = upload_file()
    if raw_df is None:
        return
 
    show_raw_preview(raw_df)
 
    if st.button("🧹 Clean Data", type="primary"):
        with st.spinner("Cleaning data..."):
            clean_df, report = clean_data(raw_df)
        st.session_state["clean_df"] = clean_df
        st.session_state["report"] = report
        st.session_state["file_name"] = file_name
 
    # Persist results across reruns (e.g. after clicking download)
    if "clean_df" in st.session_state and st.session_state.get("file_name") == file_name:
        show_report(st.session_state["clean_df"], st.session_state["report"])