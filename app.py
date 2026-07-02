import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------
# PAGE SETTINGS
# ----------------------------------------------------

st.set_page_config(
    page_title="SPCL Extraction Rate Dashboard",
    page_icon="🌲",
    layout="wide"
)

st.title("SPCL Extraction Rate Dashboard")

# ----------------------------------------------------
# DROPBOX EXCEL FILE
# ----------------------------------------------------

EXCEL_URL = "https://www.dropbox.com/scl/fi/hjs8llnx5i8ogr365n2m2/SPCL_ExtractionRates_Historial_V.xlsx?rlkey=leoec8j7me4hkuyjysc8htaci&st=oyff9bin&dl=1"

# ----------------------------------------------------
# LOAD WORKBOOK
# ----------------------------------------------------

@st.cache_data(show_spinner=True)
def load_workbook():
    return pd.read_excel(EXCEL_URL, sheet_name=None, engine="openpyxl")

try:
    workbook = load_workbook()
except Exception as e:
    st.error("Unable to load the Excel workbook.")
    st.exception(e)
    st.stop()

# ----------------------------------------------------
# SELECT WORKSHEET
# ----------------------------------------------------

sheet = st.sidebar.selectbox(
    "Select Worksheet",
    list(workbook.keys())
)

df = workbook[sheet]

st.subheader(sheet)

# ----------------------------------------------------
# FILTERS
# ----------------------------------------------------

filtered = df.copy()

st.sidebar.header("Filters")

for col in filtered.columns:

    if filtered[col].dtype == "object" and filtered[col].nunique() <= 50:

        options = sorted(filtered[col].dropna().unique())

        selected = st.sidebar.multiselect(
            col,
            options,
            default=options
        )

        filtered = filtered[
            filtered[col].isin(selected)
        ]

# ----------------------------------------------------
# DATA
# ----------------------------------------------------

st.write(f"**Rows:** {len(filtered):,}")
st.write(f"**Columns:** {len(filtered.columns)}")

st.dataframe(
    filtered,
    use_container_width=True,
    height=500
)

# ----------------------------------------------------
# CHARTS
# ----------------------------------------------------

numeric = filtered.select_dtypes(include="number").columns.tolist()
categorical = filtered.select_dtypes(exclude="number").columns.tolist()

if numeric:

    st.header("Visualization")

    chart = st.selectbox(
        "Chart Type",
        ["Bar", "Line", "Scatter", "Histogram", "Box"]
    )

    y = st.selectbox("Numeric Field", numeric)

    x = None
    if categorical:
        x = st.selectbox("Category", categorical)

    if chart == "Bar" and x:

        plot = filtered.groupby(x)[y].sum().reset_index()

        fig = px.bar(plot, x=x, y=y)

    elif chart == "Line" and x:

        plot = filtered.groupby(x)[y].sum().reset_index()

        fig = px.line(plot, x=x, y=y, markers=True)

    elif chart == "Scatter" and x:

        fig = px.scatter(filtered, x=x, y=y)

    elif chart == "Histogram":

        fig = px.histogram(filtered, x=y)

    else:

        if x:
            fig = px.box(filtered, x=x, y=y)
        else:
            fig = px.box(filtered, y=y)

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# DOWNLOAD FILTERED DATA
# ----------------------------------------------------

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Data",
    csv,
    "SPCL_ExtractionRate_Filtered.csv",
    "text/csv"
)
