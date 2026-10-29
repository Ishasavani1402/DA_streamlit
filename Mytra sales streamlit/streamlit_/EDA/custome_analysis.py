import ast
import builtins
import contextlib
import io
import traceback

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from streamlit_.helper import footer, get_clean_df

ALLOWED_IMPORTS = {
    "streamlit", "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "math", "datetime", "statistics", "collections", "itertools", "re",
    "scipy", "sklearn",
}
BLOCKED_BUILTINS = {
    "open", "eval", "exec", "compile", "input", "breakpoint",
    "exit", "quit", "help", "globals", "locals", "vars",
}


def _guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name.split(".")[0] not in ALLOWED_IMPORTS:
        raise ImportError(
            f"Import of '{name}' is not allowed here. "
            f"Allowed: {', '.join(sorted(ALLOWED_IMPORTS))}"
        )
    return builtins.__import__(name, globals, locals, fromlist, level)


def _safe_builtins() -> dict:
    safe = {k: v for k, v in vars(builtins).items() if k not in BLOCKED_BUILTINS}
    safe["__import__"] = _guarded_import
    return safe


def _check_code(tree: ast.AST) -> None:
    """Reject dunder tricks like ().__class__.__bases__ and blocked names."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            raise ValueError(f"Access to '{node.attr}' is not allowed.")
        if isinstance(node, ast.Name) and node.id in BLOCKED_BUILTINS:
            raise ValueError(f"'{node.id}' is not allowed here.")

def _is_st_call(node: ast.AST) -> bool:
    """True for expressions like st.dataframe(x) or st.sidebar.write(x)."""
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    while isinstance(func, ast.Attribute):
        func = func.value
    return isinstance(func, ast.Name) and func.id == "st"



def run_user_code(code: str, df: pd.DataFrame) -> dict:
    """Run `code` against a copy of df. Returns a dict of outputs (never raises)."""
    out = {"value": None, "stdout": "", "plotly": [], "mpl": [], "error": None,
           "uses_st": False}

    try:
        tree = ast.parse(code, mode="exec")
        _check_code(tree)

        # If the code calls st.dataframe(), st.write() ... they draw live on the page.
        out["uses_st"] = any(
            isinstance(n, ast.Name) and n.id == "st" for n in ast.walk(tree)
        )

        # Notebook style: if the last line is a bare expression, keep its value.
        # (Skip it when the line is an st.* call: those draw themselves.)
        if (
            tree.body
            and isinstance(tree.body[-1], ast.Expr)
            and not _is_st_call(tree.body[-1].value)
        ):
            last = tree.body[-1]
            assign = ast.Assign(
                targets=[ast.Name(id="_last_value", ctx=ast.Store())],
                value=last.value,
            )
            tree.body[-1] = ast.copy_location(assign, last)
            ast.fix_missing_locations(tree)

        namespace = {
            "__builtins__": _safe_builtins(),
            "df": df.copy(),
            "pd": pd, "np": np, "px": px, "plt": plt, "sns": sns, "st": st,
        }

        plt.close("all")
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            exec(compile(tree, "<your_code>", "exec"), namespace)
        out["stdout"] = buffer.getvalue()

        # 1) table / value
        value = namespace.get("result")
        if value is None:
            value = namespace.get("_last_value")
        # Never print Streamlit's own objects (e.g. result = st.dataframe(...))
        if isinstance(value, DeltaGenerator):
            value = None
        out["value"] = value

        # 2) plotly figures (any variable holding one), without duplicates
        seen = set()
        for v in namespace.values():
            if isinstance(v, go.Figure) and id(v) not in seen:
                seen.add(id(v))
                out["plotly"].append(v)

        # 3) matplotlib / seaborn figures
        out["mpl"] = [plt.figure(n) for n in plt.get_fignums()]

    except SyntaxError as e:
        out["error"] = f"Syntax error on line {e.lineno}: {e.msg}"
    except Exception:
        # keep only the part of the traceback that concerns the user's code
        tb = traceback.format_exc().splitlines()
        start = next((i for i, l in enumerate(tb) if "<your_code>" in l), 0)
        out["error"] = "\n".join([tb[0]] + tb[start:])

    return out

# Show the outputs

def _to_dataframe(value):
    """Turn Series / list / dict / array into a DataFrame, else return None."""
    if isinstance(value, pd.DataFrame):
        return value
    if isinstance(value, pd.Series):
        return value.rename(value.name or "value").reset_index()
    if isinstance(value, (list, tuple, dict, np.ndarray)):
        try:
            return pd.DataFrame(value)
        except Exception:
            return None
    return None


def show_value(value) -> None:
    table = _to_dataframe(value)
    if table is not None:
        st.caption(f"{table.shape[0]:,} rows × {table.shape[1]} columns")
        st.dataframe(table)
        st.download_button(
            "⬇️ Download result (CSV)",
            data=table.to_csv(index=False).encode("utf-8"),
            file_name="custom_analysis_result.csv",
            mime="text/csv",
            key="ca_download",
        )
    elif value is not None:
        st.write(value)


def show_outputs(out: dict) -> None:
    if out["error"]:
        st.error("Your code raised an error:")
        st.code(out["error"], language="text")
        return

    shown_anything = False

    if out["value"] is not None:
        st.subheader("Result")
        show_value(out["value"])
        shown_anything = True

    if out["plotly"] or out["mpl"]:
        st.subheader("Charts")
        for i, fig in enumerate(out["plotly"]):
            st.plotly_chart(fig, key=f"ca_plotly_{i}")
        for fig in out["mpl"]:
            st.pyplot(fig)
        shown_anything = True

    if out["stdout"].strip():
        st.subheader("Printed output")
        st.code(out["stdout"], language="text")
        shown_anything = True

    if not shown_anything and not out.get("uses_st"):
        st.info(
            "Code ran fine but there is nothing to show. "
            "Assign a table to `result`, a chart to `fig`, or use `print()`."
        )

# Page

EXAMPLES = {
    "Top 10 products by revenue": '''result = (
    df.groupby("product_name", as_index=False)
      .agg(total_revenue=("total_amount", "sum"),
           orders=("order_id", "count"))
      .sort_values("total_revenue", ascending=False)
      .head(10)
)''',
    "Cancelled / returned rate by category": '''bad = df["order_status"].isin(["Cancelled", "Returned"])
result = (
    df.assign(bad_order=bad)
      .groupby("category", as_index=False)
      .agg(total_orders=("order_id", "count"),
           bad_orders=("bad_order", "sum"))
      .assign(bad_rate_pct=lambda t: (t["bad_orders"] / t["total_orders"] * 100).round(2))
      .sort_values("bad_rate_pct", ascending=False)
)''',
    "Average rating by brand (min 30 orders)": '''result = (
    df.groupby("brand", as_index=False)
      .agg(orders=("order_id", "count"), avg_rating=("rating", "mean"))
      .query("orders >= 30")
      .round({"avg_rating": 2})
      .sort_values("avg_rating", ascending=False)
)''',
    "Revenue by payment mode (seaborn chart)": '''pay = df.groupby("payment_mode", as_index=False)["total_amount"].sum()
plt.figure(figsize=(8, 4))
sns.barplot(data=pay, x="payment_mode", y="total_amount")
plt.xticks(rotation=30)
plt.title("Revenue by Payment Mode")
result = pay''',
}
DEFAULT_CODE = EXAMPLES["Top 10 products by revenue"]


def _load_example() -> None:
    choice = st.session_state.get("ca_example")
    if choice in EXAMPLES:
        st.session_state["ca_code"] = EXAMPLES[choice]


def custom_analysis(df: pd.DataFrame) -> None:
    st.subheader("Write your Python Analysis")

    with st.expander("📋 Available columns in df"):
        cols = pd.DataFrame({
            "column": df.columns,
            "dtype": df.dtypes.astype(str).values,
        })
        st.dataframe(cols)

    st.selectbox(
        "Start from an example (optional)",
        options=["— choose an example —"] + list(EXAMPLES),
        key="ca_example",
        on_change=_load_example,
    )

    st.session_state.setdefault("ca_code", DEFAULT_CODE)
    st.text_area(
        "Your Python code",
        key="ca_code",
        height=280,
        help="Press Ctrl+Enter to apply your edit, then click Run.",
    )

    clicked = st.button("▶️ Run Analysis", type="secondary")

    # Anything your code draws with st.dataframe / st.write / st.plotly_chart
    # appears live inside this box, right under the Run button.
    live_box = st.container()

    if clicked:
        with live_box:
            with st.spinner("Running your code..."):
                st.session_state["ca_output"] = run_user_code(
                    st.session_state["ca_code"], df
                )

    # Outputs stay on screen after reruns (e.g. clicking the download button)
    if "ca_output" in st.session_state:
        show_outputs(st.session_state["ca_output"])
        st.divider()


def render_custom_analysis() -> None:
    df = get_clean_df()
    if df is None:
        st.warning("upload an already clean CSV.")
        return
    custom_analysis(df)
    footer()