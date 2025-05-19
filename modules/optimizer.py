def calculate_reorder_point(avg_daily_demand, lead_time_days, safety_stock):
    """
    Reorder Point = (Average Daily Demand × Lead Time) + Safety Stock
    """
    return (avg_daily_demand * lead_time_days) + safety_stock
