
import streamlit as st
import pandas as pd
from db import run
from .helpers import footer


def sql_runner():
    st.subheader("💻 SQL Runner")

    st.caption("Write and execute SQL queries on your clean_sales dataset.")

    query = st.text_area(
        "Write SQL Query",
        value="SELECT * FROM clean_sales LIMIT 10;",
        height=180,
        placeholder="SELECT * FROM clean_sales;"
    )

    if st.button("▶️ Run Query", use_container_width=True):
        if not query.strip():
            st.warning("Please enter a SQL query.")
        else:
            try:
                df = run(query)

                if df.empty:
                    st.info("Query executed successfully, but no data was returned.")
                else:
                    st.success(f"Query executed successfully! {len(df):,} rows returned.")

                    # Display query results
                    st.subheader("📊 Query Results")
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )

                    # Download results
                    csv = df.to_csv(index=False).encode("utf-8")

                    st.download_button(
                        label="⬇️ Download Results as CSV",
                        data=csv,
                        file_name="sql_query_results.csv",
                        mime="text/csv"
                    )

            except Exception as e:
                st.error(f"❌ SQL Error: {e}")

    footer()
