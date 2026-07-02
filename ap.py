import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="SPCL Historical Extraction Rates Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# DROPBOX FILE
# ---------------------------------------------------

FILE_URL = "https://www.dropbox.com/scl/fi/hjs8llnx5i8ogr365n2m2/SPCL_ExtractionRates_Historial_V.xlsx?rlkey=leoec8j7me4hkuyjysc8htaci&st=24y1pp7b&dl=1"

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_excel():
    sheets = pd.read_excel(FILE_URL, sheet_name=None)
    return sheets

try:
    workbook = load_excel()
except Exception as e:
    st.error(f"Unable to load workbook.\n\n{e}")
    st.stop()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Navigation")

sheet = st.sidebar.selectbox(
    "Worksheet",
    list(workbook.keys())
)

df = workbook[sheet]

st.title("SPCL Historical Extraction Rates Dashboard")
st.subheader(sheet)

st.write(f"Rows: {len(df):,}")
st.write(f"Columns: {len(df.columns)}")

# ---------------------------------------------------
# FILTERS
# ---------------------------------------------------

st.sidebar.header("Filters")

filtered = df.copy()

for col in df.columns:

    if (
        df[col].dtype == "object"
        and df[col].nunique() <= 30
    ):
        values = sorted(df[col].dropna().unique())

        selected = st.sidebar.multiselect(
            col,
            values,
            default=values
        )

        filtered = filtered[
            filtered[col].isin(selected)
        ]

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------

st.dataframe(
    filtered,
    use_container_width=True,
    height=500
)

# ---------------------------------------------------
# NUMERIC COLUMNS
# ---------------------------------------------------

numeric_cols = filtered.select_dtypes(include="number").columns.tolist()

categorical_cols = filtered.select_dtypes(exclude="number").columns.tolist()

# ---------------------------------------------------
# CHARTS
# ---------------------------------------------------

if len(numeric_cols) > 0:

    st.header("Visualizations")

    chart_type = st.selectbox(
        "Chart Type",
        ["Bar", "Line", "Scatter", "Histogram", "Box Plot"]
    )

    if len(categorical_cols) > 0:
        x = st.selectbox(
            "Category",
            categorical_cols
        )
    else:
        x = None

    y = st.selectbox(
        "Value",
        numeric_cols
    )

    if chart_type == "Bar" and x:

        plot = (
            filtered
            .groupby(x)[y]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            plot,
            x=x,
            y=y
        )

    elif chart_type == "Line" and x:

        plot = (
            filtered
            .groupby(x)[y]
            .sum()
            .reset_index()
        )

        fig = px.line(
            plot,
            x=x,
            y=y,
            markers=True
        )

    elif chart_type == "Scatter" and x:

        fig = px.scatter(
            filtered,
            x=x,
            y=y
        )

    elif chart_type == "Histogram":

        fig = px.histogram(
            filtered,
            x=y
        )

    elif chart_type == "Box Plot":

        if x:
            fig = px.box(
                filtered,
                x=x,
                y=y
            )
        else:
            fig = px.box(
                filtered,
                y=y
            )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------
# DOWNLOAD
# ---------------------------------------------------

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Data",
    csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)
