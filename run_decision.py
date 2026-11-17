"""Reproduce the saved portfolio baseline and the existing cost stress."""
import json
from pathlib import Path

from portfolio import estimate, largest_change, search

root = Path(__file__).resolve().parent
mandate = json.loads((root / "project2_mandate.json").read_text())
data = estimate(root / "prices.csv")
if data["labels"] != mandate["tickers"]:
    raise ValueError("Price columns must match mandate ticker order.")

constraints = (
    mandate["reserve_eligible"],
    mandate["objective_annual_decimal"],
    mandate["reserve_minimum"],
)
baseline = search(data["returns"], data["covariance"], *constraints)
recent_data = estimate(root / "prices.csv", last36=True)
recent = search(recent_data["returns"], recent_data["covariance"], *constraints)
annual_cost = 0.0025
net_returns = [value - annual_cost for value in data["returns"]]
stress = search(net_returns, data["covariance"], *constraints)

print(json.dumps({
    "tickers": data["labels"],
    "price_dates": [data["price_start"], data["price_end"]],
    "monthly_returns": data["observations"],
    "mandate": mandate,
    "baseline_mandate_check": "PASS" if baseline else "NO_FEASIBLE_GRID_MIX",
    "baseline": baseline,
    "last_36_months": recent,
    "window_largest_weight_change_pp": largest_change(baseline, recent),
    "stress_annual_cost_decimal": annual_cost,
    "cost_stress": stress,
    "cost_largest_weight_change_pp": largest_change(baseline, stress),
}, indent=2))
