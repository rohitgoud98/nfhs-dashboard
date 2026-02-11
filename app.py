import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="India Change Dashboard",
    layout="wide"
)

st.title("📊 India Change Dashboard")

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("/mnt/data/India_Change.csv")

df = load_data()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Filters")

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

selected_category = None
if categorical_cols:
    selected_category = st.sidebar.selectbox(
        "Select Category",
        options=["All"] + categorical_cols
    )

filtered_df = df.copy()

if selected_category and selected_category != "All":
    category_value = st.sidebar.selectbox(
        f"Select {selected_category}",
        options=filtered_df[selected_category].unique()
    )
    filtered_df = filtered_df[filtered_df[selected_category] == category_value]

# -----------------------------
# Data preview
# -----------------------------
with st.expander("🔍 View Data"):
    st.dataframe(filtered_df)

# -----------------------------
# KPI Section
# -----------------------------
st.subheader("Key Metrics")

kpi_cols = st.columns(len(numeric_cols[:4]) if numeric_cols else 1)

for i, col in enumerate(numeric_cols[:4]):
    kpi_cols[i].metric(
        label=col,
        value=round(filtered_df[col].mean(), 2)
    )

# -----------------------------
# Charts
# -----------------------------
st.subheader("Visual Analysis")

if numeric_cols:
    col1, col2 = st.columns(2)

    with col1:
        selected_y = st.selectbox("Select Numeric Column", numeric_cols)
        fig, ax = plt.subplots()
        ax.plot(filtered_df[selected_y])
        ax.set_title(f"{selected_y} Trend")
        ax.set_xlabel("Index")
        ax.set_ylabel(selected_y)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        ax.hist(filtered_df[selected_y], bins=20)
        ax.set_title(f"{selected_y} Distribution")
        st.pyplot(fig)

# -----------------------------
# Bar chart (if categorical + numeric)
# -----------------------------
if categorical_cols and numeric_cols:
    st.subheader("Category Comparison")

    cat_col = st.selectbox("Category Column", categorical_cols)
    num_col = st.selectbox("Numeric Column", numeric_cols)

    grouped = filtered_df.groupby(cat_col)[num_col].mean()

    fig, ax = plt.subplots()
    grouped.plot(kind="bar", ax=ax)
    ax.set_title(f"Average {num_col} by {cat_col}")
    ax.set_ylabel(num_col)

    st.pyplot(fig)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Built with Streamlit")
