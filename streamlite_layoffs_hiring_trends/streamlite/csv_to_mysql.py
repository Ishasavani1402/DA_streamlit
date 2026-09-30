import os
import sys
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv       
load_dotenv()


# ─────────────────────────────────────────────
# 1. DATABASE CONNECTION
# ─────────────────────────────────────────────
def create_connection():
    try:
        conn = mysql.connector.connect(
            host     = os.environ.get("DB_HOST",     ""),
            user     = os.environ.get("DB_USER",     ""),
            password = os.environ.get("DB_PASSWORD", ""),   # ✅ from .env
            database = os.environ.get("DB_NAME",     "")
        )
        if conn.is_connected():
            print("✅ Connected to MySQL")
        return conn
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None


# ─────────────────────────────────────────────
# 2. MAP PANDAS DTYPE → CORRECT MYSQL TYPE
# ─────────────────────────────────────────────
def get_mysql_type(col, dtype):
    """
    ✅ Fix 3: Use DECIMAL(10,2) for financial/percentage columns
               instead of FLOAT — prevents silent rounding errors.
    """
    decimal_cols = [
        'layoff_percentage',
        'revenue_growth_percent',
        'salary_budget_change',
        'stock_growth_percent',
        'remote_jobs_percentage',
        'ai_replacement_risk',
        'ai_automation_impact',
        'ai_adoption_level',
        'employee_sentiment',
        'job_security_score',
    ]
    if col in decimal_cols:        return "DECIMAL(10,2)"
    if "int"      in str(dtype):   return "INT"
    if "float"    in str(dtype):   return "FLOAT"
    if "datetime" in str(dtype):   return "DATETIME"
    if "object"   in str(dtype):   return "VARCHAR(255)"
    return "TEXT"


# ─────────────────────────────────────────────
# 3. SAFE NULL HANDLING
# ─────────────────────────────────────────────
def safe_fillna(df):
    """
    ✅ Fix 2: Handle nulls separately per dtype.
               Old code: df.fillna("") → puts empty string in FLOAT cols
               → MySQL silently stores 0 instead of NULL.
    """
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    str_cols = df.select_dtypes(include=['object']).columns

    # numeric nulls → stay as None (MySQL NULL)
    df[num_cols] = df[num_cols].where(df[num_cols].notna(), None)

    # string nulls → empty string
    df[str_cols] = df[str_cols].fillna("")

    return df


# ─────────────────────────────────────────────
# 4. CREATE TABLE FROM CSV SCHEMA
# ─────────────────────────────────────────────
def create_table_from_csv(cursor, table_name, df):
    columns = []
    for col, dtype in zip(df.columns, df.dtypes):
        mysql_type = get_mysql_type(col, dtype)          # ✅ uses correct type mapper
        columns.append(f"`{col}` {mysql_type}")

    columns_sql = ", ".join(columns)

    cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")

    create_table_query = f"""
        CREATE TABLE `{table_name}` (
            {columns_sql}
        );
    """
    cursor.execute(create_table_query)
    print(f"📌 Table `{table_name}` created.")


# ─────────────────────────────────────────────
# 5. INSERT CSV DATA INTO MYSQL
# ─────────────────────────────────────────────
def insert_data(cursor, conn, table_name, df):
    placeholders = ", ".join(["%s"] * len(df.columns))
    columns      = ", ".join([f"`{col}`" for col in df.columns])
    insert_query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"

    df = safe_fillna(df)                                 # ✅ Fix 2 applied here

    total_rows = len(df)
    inserted   = 0

    for i in range(0, total_rows, 1000):
        chunk = df.iloc[i:i + 1000]
        # convert to list of tuples; replace pandas NA with Python None
        data  = [
            tuple(None if pd.isna(v) else v for v in row)
            for row in chunk.values
        ]
        cursor.executemany(insert_query, data)
        conn.commit()
        inserted += len(chunk)
        print(f"   ↳ Inserted {inserted}/{total_rows} rows...", end="\r")

    print(f"\n🚀 Data inserted into `{table_name}` ({inserted} rows total)")


# ─────────────────────────────────────────────
# 6. LOAD A SINGLE CSV → MYSQL
# ─────────────────────────────────────────────
def load_single_csv_to_mysql(file_path, conn):
    cursor     = conn.cursor()
    table_name = os.path.basename(file_path).replace(".csv", "").lower()

    print(f"\n📂 Processing: {file_path}")

    df = pd.read_csv(file_path)
    print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")

    create_table_from_csv(cursor, table_name, df)
    insert_data(cursor, conn, table_name, df)

    cursor.close()


# ─────────────────────────────────────────────
# 7. MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":

    # ✅ Fix 1: path from .env or command-line arg — not hardcoded
    CSV_FILE = (
        os.environ.get("CSV_FILE")                        # option A: set in .env
        or (sys.argv[1] if len(sys.argv) > 1 else None)  # option B: python csv_to_mysql.py path/to/file.csv
    )

    if not CSV_FILE:
        print("❌ No CSV file specified.")
        print("   Set CSV_FILE in your .env  OR  pass path as argument:")
        print("   python csv_to_mysql.py path/to/file.csv")
        sys.exit(1)

    if not os.path.exists(CSV_FILE):
        print(f"❌ File not found: {CSV_FILE}")
        sys.exit(1)

    connection = create_connection()

    if connection:
        load_single_csv_to_mysql(CSV_FILE, connection)
        connection.close()
        print("\n🎉 CSV loaded successfully into MySQL!")