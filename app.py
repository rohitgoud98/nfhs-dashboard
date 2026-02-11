import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="India NFHS Change Dashboard",
    layout="wide"
)

st.title("📊 India NFHS-4 vs NFHS-5 Change Dashboard")

# ----------------------------------
# Load Data
# ----------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("India_Change.csv")

df = load_data()

# ----------------------------------
# Sidebar Filters
# ----------------------------------
st.sidebar.header("Filters")

state = st.sidebar.selectbox(
    "Select State",
    sorted(df["State"].unique())
)

districts = df[df["State"] == state]["District Name"].unique()
district = st.sidebar.selectbox(
    "Select District",
    sorted(districts)
)

categories = df[
    (df["State"] == state) &
    (df["District Name"] == district)
]["Category"].unique()

category = st.sidebar.selectbox(
    "Select Category",
    categories
)

indicators = df[
    (df["State"] == state) &
    (df["District Name"] == district) &
    (df["Category"] == category)
]["Indicator"].unique()

indicator = st.sidebar.selectbox(
    "Select Indicator",
    indicators
)

# ----------------------------------
# Filtered Row
# ----------------------------------
filtered_df = df[
    (df["State"] == state) &
    (df["District Name"] == district) &
    (df["Category"] == category) &
    (df["Indicator"] == indicator)
]

row = filtered_df.iloc[0]

nfhs4 = row["NFHS 4"]
nfhs5 = row["NFHS 5"]
change = row["Change"]

# ----------------------------------
# KPI Metrics
# ----------------------------------
st.subheader("Key Indicators")

c1, c2, c3 = st.columns(3)
c1.metric("NFHS-4 (%)", f"{nfhs4}")
c2.metric("NFHS-5 (%)", f"{nfhs5}")
c3.metric("Change (%)", f"{change}", delta=f"{change}%")

# ----------------------------------
# NFHS Comparison Chart
# ----------------------------------
st.subheader("NFHS Comparison")

compare_df = pd.DataFrame({
    "Survey": ["NFHS-4", "NFHS-5"],
    "Value": [nfhs4, nfhs5]
})

fig1 = px.bar(
    compare_df,
    x="Survey",
    y="Value",
    text="Value",
    title=indicator
)

fig1.update_traces(textposition="outside")
fig1.update_layout(yaxis_title="Percentage")

st.plotly_chart(fig1, use_container_width=True)

# ----------------------------------
# Category Overview (District Level)
# ----------------------------------
st.subheader("Indicator-wise Change (District Level)")

overview = df[
    (df["State"] == state) &
    (df["District Name"] == district) &
    (df["Category"] == category)
]

fig2 = px.bar(
    overview,
    x="Change",
    y="Indicator",
    orientation="h",
    color="Change",
    title=f"Change in {category}",
    labels={"Change": "Change (%)"}
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------
# Data Table
# ----------------------------------
with st.expander("📄 View Data"):
    st.dataframe(overview)

# ----------------------------------
# Footer
# ----------------------------------
st.markdown("---")
st.caption("Source: NFHS-4 & NFHS-5 | Built with Streamlit & Plotly")
