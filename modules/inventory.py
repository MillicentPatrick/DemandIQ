import streamlit as st
import matplotlib.pyplot as plt

def run_inventory(df):
    st.subheader(" Inventory Planning")

    avg_demand = df['Units Sold'].mean()
    lead_time = st.slider("Lead Time (days)", 1, 30, 7)
    safety_stock = st.slider("Safety Stock (units)", 0, 500, 50)

    reorder_point = int((avg_demand * lead_time) + safety_stock)
    st.metric("Reorder Point", reorder_point)

    # Inventory simulator
    st.write("### What-if Analysis")
    days = list(range(1, 31))
    demand_projection = [avg_demand * d for d in days]
    inventory_levels = [reorder_point - d for d in demand_projection]

    fig, ax = plt.subplots()
    ax.plot(days, inventory_levels, label="Projected Inventory")
    ax.axhline(y=safety_stock, color='r', linestyle='--', label='Safety Stock Threshold')
    ax.set_xlabel("Days")
    ax.set_ylabel("Inventory Level")
    ax.set_title("Inventory Depletion Over Time")
    ax.legend()
    st.pyplot(fig)
