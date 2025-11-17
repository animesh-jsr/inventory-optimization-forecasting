import os
import pandas as pd
from ortools.linear_solver import pywraplp

def optimize_inventory(forecast_df):
    forecast = forecast_df['forecast'].tolist()

    holding_cost = 2     # ₹ per unit
    stockout_cost = 10   # ₹ per unit
    safety_factor = 1.65 # For 95% service level (unused here but can be applied)

    solver = pywraplp.Solver.CreateSolver('GLOP')

    # Variables
    order_qty = [solver.NumVar(0, solver.infinity(), f'Q_{i}') for i in range(len(forecast))]
    safety_stock = solver.NumVar(0, solver.infinity(), 'safety_stock')

    # Objective: Minimize holding + stockout cost
    objective = solver.Objective()
    for i in range(len(forecast)):
        objective.SetCoefficient(order_qty[i], holding_cost)

    objective.SetCoefficient(safety_stock, stockout_cost)
    objective.SetMinimization()

    # Constraints: Order must satisfy demand + safety stock
    for i in range(len(forecast)):
        solver.Add(order_qty[i] >= forecast[i] + safety_stock)

    solver.Solve()

    results = pd.DataFrame({
        "Forecast": forecast,
        "Order_Quantity": [order_qty[i].solution_value() for i in range(len(forecast))]
    })

    # Ensure results directory exists
    results_dir = "../results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Save results
    results.to_csv("../results/inventory_plan.csv", index=False)

    return results
