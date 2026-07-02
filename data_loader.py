import pandas as pd
import streamlit as st

EXCEL_URL = (
    "https://www.dropbox.com/scl/fi/hjs8llnx5i8ogr365n2m2/"
    "SPCL_ExtractionRates_Historial_V.xlsx"
    "?rlkey=leoec8j7me4hkuyjysc8htaci"
    "&st=oyff9bin"
    "&dl=1"
)


@st.cache_data(show_spinner=True)
def load_data():

    workbook = pd.read_excel(
        EXCEL_URL,
        sheet_name=None,
        engine="openpyxl"
    )

    df = None

    for sheet_name, sheet in workbook.items():

        cols = [str(c).strip() for c in sheet.columns]

        if "Date" in cols and "Extraction Rate" in cols:

            df = sheet.copy()
            break

    if df is None:
        raise ValueError(
            "Could not find a worksheet containing "
            "'Date' and 'Extraction Rate' columns."
        )

    df.columns = df.columns.str.strip()

    df["Date"] = pd.to_datetime(df["Date"])

    df["Extraction Rate"] = pd.to_numeric(
        df["Extraction Rate"],
        errors="coerce"
    )

    df = df.dropna(subset=["Date", "Extraction Rate"])

    df["Year"] = df["Date"].dt.year

    df = df.sort_values("Date")

    return df
