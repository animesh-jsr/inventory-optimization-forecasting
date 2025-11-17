import os
from forecast import forecast_demand
from optimize_inventory import optimize_inventory

def main():

    # Ensure results folder exists
    results_path = "../results"
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    # Run forecasting
    forecast = forecast_demand("../data/historical_demand.csv", forecast_periods=6)

    # Run inventory optimization
    inventory_plan = optimize_inventory(forecast)

    # Print outputs
    print("\n================= DEMAND FORECAST =================\n")
    print(forecast)

    print("\n================= INVENTORY PLAN ==================\n")
    print(inventory_plan)

if __name__ == "__main__":
    main()
