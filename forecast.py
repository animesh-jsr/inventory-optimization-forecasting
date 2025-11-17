import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def forecast_demand(data_path, forecast_periods=6):

    # Load demand data
    df = pd.read_csv(data_path)
    df['month'] = pd.to_datetime(df['month'])
    df.set_index('month', inplace=True)

    # NON-seasonal model (because you have < 24 months data)
    model = ExponentialSmoothing(
        df['demand'],
        trend='add',
        seasonal=None
    ).fit()

    # Forecast next n periods
    forecast = model.forecast(forecast_periods)
    forecast_df = pd.DataFrame({"forecast": forecast})

    # Ensure results folder exists
    results_dir = "../results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Save forecast CSV
    forecast_df.to_csv("../results/forecast_output.csv")

    # Plot forecast
    plt.figure(figsize=(8,4))
    plt.plot(df.index, df['demand'], label="Historical Demand")
    plt.plot(forecast.index, forecast, linestyle='--', label="Forecast")
    plt.title("Demand Forecast")
    plt.xlabel("Month")
    plt.ylabel("Demand")
    plt.legend()
    plt.tight_layout()
    plt.savefig("../results/forecast_plot.png", dpi=300)

    return forecast_df
