from prophet import Prophet
import pandas as pd
import plotly.graph_objects as go

def forecast_demand(df, periods=90, extra_regressors=None):
    df = df.rename(columns={"Date": "ds", "Units Sold": "y"})
    df = df[["ds", "y"] + (extra_regressors or [])].copy()

    if "Promo" in df.columns:
        df["Promo"] = df["Promo"].map({"Yes": 1, "No": 0})
    if "Price" in df.columns:
        df["Price"] = pd.to_numeric(df["Price"], errors='coerce')

    df = df.dropna()

    model = Prophet()
    if extra_regressors:
        for reg in extra_regressors:
            model.add_regressor(reg)

    model.fit(df)

    future = model.make_future_dataframe(periods=periods)
    for reg in (extra_regressors or []):
        full = pd.concat([df[["ds", reg]], future], axis=0)
        future[reg] = full[reg].ffill().bfill().values[:len(future)]

    forecast = model.predict(future)
    return model, forecast

def plot_forecast(original_df, forecast):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=original_df['ds'], y=original_df['y'], name='Actual'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], name='Upper Bound', line=dict(dash='dot')))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], name='Lower Bound', line=dict(dash='dot')))
    fig.update_layout(title='Forecast with Prophet', xaxis_title='Date', yaxis_title='Units Sold')
    return fig
