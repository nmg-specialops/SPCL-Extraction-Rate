import streamlit as st
from data_loader import load_data
from calculations import (
    calculate_kpis,
    annual_summary,
    filter_data,
)
from charts import (
    extraction_rate_chart,
    moving_average_chart,
)

# --------------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------------

st.set_page_config(
    page_title="SPCL Extraction Rate Dashboard",
    page_icon="📈",
    layout="wide",
)

# --------------------------------------------------------
# LOAD DATA
# --------------------------------------------------------

df = load_data()

# --------------------------------------------------------
# SIDEBAR
# --------------------------------------------------------

st.sidebar.title("SPCL Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Extraction Trends",
        "Annual Summary",
        "Data Explorer",
    ],
)

# -----------------------------
# YEAR FILTER
# -----------------------------

years = sorted(df["Year"].unique())

selected_years = st.sidebar.multiselect(
    "Year",
    years,
    default=years,
)

filtered = filter_data(df, selected_years)

# --------------------------------------------------------
# OVERVIEW
# --------------------------------------------------------

if page == "Overview":

    st.title("SPCL Extraction Rate Dashboard")

    st.markdown(
        "Historical Extraction Rates"
    )

    kpi = calculate_kpis(filtered)

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Records",
        f"{kpi['records']:,}"
    )

    c2.metric(
        "Average",
        f"{kpi['average']:.2%}"
    )

    c3.metric(
        "Highest",
        f"{kpi['highest']:.2%}"
    )

    c4.metric(
        "Lowest",
        f"{kpi['lowest']:.2%}"
    )

    c5.metric(
        "Latest",
        f"{kpi['latest']:.2%}"
    )

    st.divider()

    fig = extraction_rate_chart(filtered)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------------
# EXTRACTION TRENDS
# --------------------------------------------------------

elif page == "Extraction Trends":

    st.title("Extraction Trends")

    tab1, tab2 = st.tabs(
        [
            "Historical Trend",
            "Moving Average",
        ]
    )

    with tab1:

        fig = extraction_rate_chart(filtered)

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with tab2:

        window = st.slider(
            "Moving Average Window",
            2,
            10,
            5,
        )

        fig = moving_average_chart(
            filtered,
            window,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

# --------------------------------------------------------
# ANNUAL SUMMARY
# --------------------------------------------------------

elif page == "Annual Summary":

    st.title("Annual Summary")

    summary = annual_summary(filtered)

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True,
    )

    csv = summary.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Annual Summary",
        csv,
        "Annual_Summary.csv",
        "text/csv",
    )

# --------------------------------------------------------
# DATA EXPLORER
# --------------------------------------------------------

elif page == "Data Explorer":

    st.title("Data Explorer")

    search = st.text_input(
        "Search Date"
    )

    if search:

        table = filtered[
            filtered["Date"]
            .astype(str)
            .str.contains(
                search,
                case=False,
            )
        ]

    else:

        table = filtered

    st.dataframe(
        table,
        use_container_width=True,
        height=700,
        hide_index=True,
    )

    csv = table.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Filtered Data",
        csv,
        "ExtractionRateData.csv",
        "text/csv",
    )
