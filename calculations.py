import pandas as pd


# --------------------------------------------------------
# FILTER DATA
# --------------------------------------------------------

def filter_data(df, selected_years):

    if selected_years:
        return df[df["Year"].isin(selected_years)]

    return df


# --------------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------------

def calculate_kpis(df):

    rate = df["Extraction Rate"]

    latest = rate.iloc[-1]

    return {

        "records": len(df),

        "average": rate.mean(),

        "highest": rate.max(),

        "lowest": rate.min(),

        "latest": latest

    }


# --------------------------------------------------------
# ANNUAL SUMMARY
# --------------------------------------------------------

def annual_summary(df):

    summary = (

        df

        .groupby("Year")

        .agg(

            Average_Extraction_Rate=("Extraction Rate","mean"),

            Highest_Extraction_Rate=("Extraction Rate","max"),

            Lowest_Extraction_Rate=("Extraction Rate","min"),

            Records=("Extraction Rate","count")

        )

        .reset_index()

    )

    return summary
