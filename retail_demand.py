import streamlit as st
import pandas as pd
import os

from modules.eda import run_eda
from modules.forecast import forecast_demand, plot_forecast
from modules.inventory import run_inventory
from utils.helpers import generate_report

# App Configuration
st.set_page_config(page_title="DemandIQ – Retail Demand Forecasting", layout="wide")
st.image("assets/logo.png", width=150)  # ensure your logo is at assets/logo.png
st.title(" DemandIQ – Retail Demand Forecasting and Inventory Planner")

# Load data
def load_data():
    try:
        df = pd.read_csv("data/sample_data.csv")
    except:
        st.error("Sample data missing!")
        return pd.DataFrame()
    return df

uploaded_file = st.file_uploader("Upload your retail CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Using sample data for demo.")
    df = load_data()

if df.empty:
    st.stop()

# Ensure required columns are present
required_cols = {"Date", "ProductID", "Product Name", "Units Sold", "Price", "Promo"}
if not required_cols.issubset(df.columns):
    st.error("Dataset must contain columns: " + ", ".join(required_cols))
    st.stop()

# Preprocess
df["Date"] = pd.to_datetime(df["Date"])

# Sidebar filters
products = df["Product Name"].unique()
selected_product = st.sidebar.selectbox("Select Product", products)

filtered_df = df[df["Product Name"] == selected_product].sort_values("Date")

# Main Tabs
tab1, tab2, tab3 = st.tabs([" EDA", " Forecasting", " Inventory"])

with tab1:
    run_eda(filtered_df)

with tab2:
    st.subheader(f"Forecast for {selected_product}")
    use_price = st.checkbox("Use Price as Regressor")
    use_promo = st.checkbox("Use Promo as Regressor")

    regressors = []
    if use_price:
        regressors.append("Price")
    if use_promo:
        regressors.append("Promo")

    model, forecast = forecast_demand(filtered_df, periods=90, extra_regressors=regressors)
    fig = plot_forecast(filtered_df.rename(columns={"Date": "ds", "Units Sold": "y"}), forecast)
    st.plotly_chart(fig, use_container_width=True)

    # PDF Report
    if st.button(" Download PDF Report"):
        pdf = generate_report(filtered_df, forecast, selected_product)
        st.download_button("Download Report", pdf, file_name=f"{selected_product}_forecast.pdf")

with tab3:
    run_inventory(filtered_df)

