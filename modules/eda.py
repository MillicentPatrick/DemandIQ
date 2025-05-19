# modules/eda.py

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def run_eda(df):
    st.subheader(" Exploratory Data Analysis")

    # Ensure Date column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Daily Demand Trend
    st.write("###  Daily Demand Trend")

    daily_demand = (
        df.groupby('Date')['Units Sold']
        .sum()
        .reset_index()
        .sort_values('Date')
    )

    if daily_demand.empty:
        st.warning("No daily demand data to display.")
    else:
        daily_demand = daily_demand.set_index('Date')
        st.line_chart(daily_demand)

    # Demand by Product
    st.write("###  Demand by Product")
    demand_by_product = df.groupby('Product Name')['Units Sold'].sum().sort_values(ascending=False)
    st.bar_chart(demand_by_product)

    # Seasonality Heatmap
    st.write("###  Seasonality Heatmap")
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.dayofweek  # 0 = Monday

    pivot = df.pivot_table(index='Day', columns='Month', values='Units Sold', aggfunc='sum')

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(pivot, cmap="YlGnBu", annot=True, fmt=".0f", linewidths=0.5, ax=ax)
    ax.set_title("Units Sold by Day of Week and Month")
    st.pyplot(fig)
