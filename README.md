# DemandIQ – Retail Demand Forecasting & Inventory Planner

DemandIQ is a Streamlit web app that helps retail businesses forecast demand, detect anomalies, and simulate inventory requirements.

##  Features

- Upload your retail sales data (CSV/Excel)
- EDA: Trends, seasonality, correlation
- Prophet-based forecasting (with Promo/Price regressors)
- Anomaly detection with Z-score
- Inventory optimization
- PDF summary report generation and downloading

## Tech Stack

- Python, pandas, Prophet, Streamlit, Plotly
- PDF export using `xhtml2pdf`

##  Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py

link:https://demandiq-5mfck2wu56ay9qrp2rvxbc.streamlit.app/
