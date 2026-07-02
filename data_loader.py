import pandas as pd
import streamlit as st

# --------------------------------------------------------
# DROPBOX EXCEL FILE
# --------------------------------------------------------

EXCEL_URL = (
    "https://www.dropbox.com/scl/fi/hjs8llnx5i8ogr365n2m2/"
    "SPCL_ExtractionRates_Historial_V.xlsx"
    "?rlkey=leoec8j7me4hkuyjysc8htaci"
    "&st=oyff9bin"
    "&dl=1"
)

# --------------------------------------------------------
# LOAD DATA
# --------------------------------------------------------

@st.cache_data(show_spinner=True)
def load_data():

    df = pd.read_excel(
        EXCEL_URL,
        engine="openpyxl"
    )

    # Clean column names
    df.columns = df.columns.str.strip()

    # Date column
    df["Date"] = pd.to_datetime(df["Date"])

    # Year column for filtering
    df["Year"] = df["Date"].dt.year

    # Sort oldest → newest
    df = df.sort_values("Date")

    return df
