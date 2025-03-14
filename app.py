import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Cohort Analysis Dashboard", layout="wide")

# Title
st.title("Cohort Analysis Dashboard")

# Upload dataset
uploaded_file = st.file_uploader("Upload your cohort analysis dataset (CSV)", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Calculate retention rates
    retention_rates = df.iloc[:, 1:].div(df["Month 1"], axis=0) * 100
    retention_rates["Cohort (Signup Month)"] = df["Cohort (Signup Month)"]

    # Melt the data for line and area charts
    melted_data = pd.melt(
        retention_rates,
        id_vars=["Cohort (Signup Month)"],
        var_name="Month",
        value_name="Retention Rate"
    )
    melted_data["Month"] = melted_data["Month"].str.extract('(\d+)').astype(int)

    # Sidebar for cohort selection
    st.sidebar.header("Cohort Selection")
    all_cohorts = df["Cohort (Signup Month)"].unique()
    selected_cohorts = st.sidebar.multiselect(
        "Select cohorts to analyze",
        all_cohorts,
        default=all_cohorts[:5]  # Default to first 5 cohorts
    )

    # Visualization 1: Heatmap
    st.header("Retention Heatmap")
    plt.figure(figsize=(12, 8))
    heatmap_data = retention_rates.set_index("Cohort (Signup Month)")
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5)
    plt.title("Cohort Analysis - Retention Heatmap")
    plt.xlabel("Months After Signup")
    plt.ylabel("Cohort (Signup Month)")
    st.pyplot(plt)

    # Visualization 2: Line Chart (Trends for Selected Cohorts)
    st.header("Retention Trends (Line Chart)")
    plt.figure(figsize=(12, 6))
    for cohort in selected_cohorts:
        cohort_data = melted_data[melted_data["Cohort (Signup Month)"] == cohort]
        plt.plot(cohort_data["Month"], cohort_data["Retention Rate"], label=cohort)
    plt.title("Cohort Analysis - Retention Trends (Line Chart)")
    plt.xlabel("Months After Signup")
    plt.ylabel("Retention Rate (%)")
    plt.legend(title="Cohort")
    plt.grid(True)
    st.pyplot(plt)

    # Visualization 3: Bar Chart (Retention Rates for Specific Cohorts)
    st.header("Retention Rates for Specific Cohorts (Bar Chart)")
    specific_cohort = st.selectbox("Select a cohort for bar chart", all_cohorts)
    plt.figure(figsize=(12, 6))
    cohort_data = melted_data[melted_data["Cohort (Signup Month)"] == specific_cohort]
    sns.barplot(x="Month", y="Retention Rate", data=cohort_data, palette="viridis")
    plt.title(f"Cohort Analysis - Retention Rates for {specific_cohort} (Bar Chart)")
    plt.xlabel("Months After Signup")
    plt.ylabel("Retention Rate (%)")
    st.pyplot(plt)

    # Visualization 4: Area Chart (Cumulative Retention Over Time)
    st.header("Cumulative Retention Over Time (Area Chart)")
    plt.figure(figsize=(12, 6))
    sns.lineplot(
        x="Month",
        y="Retention Rate",
        hue="Cohort (Signup Month)",
        data=melted_data,
        estimator="sum",
        ci=None,
        palette="tab20"
    )
    plt.title("Cohort Analysis - Cumulative Retention Over Time (Area Chart)")
    plt.xlabel("Months After Signup")
    plt.ylabel("Retention Rate (%)")
    plt.fill_between(
        melted_data["Month"].unique(),
        melted_data.groupby("Month")["Retention Rate"].sum(),
        color="skyblue",
        alpha=0.4
    )
    plt.legend(title="Cohort", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True)
    st.pyplot(plt)

else:
    st.info("Please upload a CSV file to get started.")