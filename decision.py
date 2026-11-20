"""Frozen evidence and committee diagnostics shared by the app and CLI."""
import csv
from datetime import date
import hashlib
import json
from pathlib import Path

import numpy as np

from portfolio import estimate, largest_change, search

ROOT = Path(__file__).resolve().parent


def assess(weights, means, covariance, floor, reserve):
    weights = np.asarray(weights)
    net_return = float(weights @ means)
    failures = []
    if net_return < floor - 1e-12:
        failures.append("Estimated net return below floor")
    if weights[2] < reserve - 1e-12:
        failures.append("SGOV reserve below minimum")
    if (weights < 0).any() or not np.isclose(weights.sum(), 1):
        failures.append("Long-only or full-investment rule")
    return {
        "weights": weights.tolist(), "return": net_return,
        "volatility": float(np.sqrt(weights @ covariance @ weights)),
        "verdict": "FAIL" if failures else "PASS", "failures": failures,
    }


def report():
    mandate = json.loads((ROOT / "project2_mandate.json").read_text())
    source = json.loads((ROOT / "price_sources.json").read_text())
    prices = ROOT / "prices.csv"
    digest = hashlib.sha256(prices.read_bytes()).hexdigest()
    if digest != source["sha256"]:
        raise ValueError("Price snapshot does not match the recorded SHA-256.")
    full = estimate(prices)
    recent = estimate(prices, last36=True)
    if full["labels"] != mandate["tickers"]:
        raise ValueError("Price columns must match the mandate.")
    floor = mandate["objective_annual_decimal"]
    reserve = mandate["reserve_minimum"]
    eligible = mandate["reserve_eligible"]

    def solve(data, drag=0, minimum=reserve):
        return search(np.asarray(data["returns"]) - drag, data["covariance"],
                      eligible, floor, minimum)

    base = solve(full)
    portfolios = {}
    choices = {"Equal weight": [1 / 3] * 3, "60/40 benchmark": [.6, .4, 0]}
    if base:
        choices["Constrained portfolio"] = base["weights"]
    for name, weights in choices.items():
        portfolios[name] = assess(weights, full["returns"], full["covariance"], floor, reserve)

    stresses = {}
    for label, data, drag, minimum in [
        ("All fund return estimates −1 pp", full, .01, reserve),
        ("Last 36 monthly returns", recent, 0, reserve),
        ("25 bp annual cost", full, .0025, reserve),
        ("50% minimum SGOV reserve", full, 0, .50),
        ("Combined stress", recent, .0125, .50),
        ("100% minimum SGOV reserve", full, 0, 1),
    ]:
        result = solve(data, drag, minimum)
        stresses[label] = {
            "result": result, "largest_weight_change_pp": largest_change(base, result),
            "observations": data["observations"], "annual_drag": drag, "minimum_reserve": minimum,
        }

    # The first evidenced availability is the download date, after the price cutoff.
    rows = list(csv.DictReader(prices.read_text().splitlines()))
    latest = rows[-1]
    prior = rows[-13]
    snapshot_ready = max(item["retrieved_utc"] for item in source["sources"])
    if date.fromisoformat(latest["date"]) >= date.fromisoformat(snapshot_ready[:10]):
        raise ValueError("Signal requires an observed price cutoff before snapshot availability.")
    vti_relative = (float(latest["VTI"]) / float(prior["VTI"])) / (
        float(latest["SGOV"]) / float(prior["SGOV"])) - 1
    # Fixed chronological split. Re-estimate through September 2025, then
    # measure the next 12 months at constant monthly rebalanced weights.
    price_lines = prices.read_text().splitlines()
    train = estimate("\n".join(price_lines[:-12]))
    trained_mix = solve(train)
    holdout = None
    if trained_mix:
        price_matrix = np.array([[float(row[ticker]) for ticker in mandate["tickers"]]
                                 for row in rows[-13:]])
        realized = (price_matrix[1:] / price_matrix[:-1] - 1) @ trained_mix["weights"]
        holdout = {
            "training_cutoff": train["price_end"],
            "evaluation_end": latest["date"],
            "weights": trained_mix["weights"],
            "gross_compounded_return": float(np.prod(1 + realized) - 1),
            "months": len(realized),
        }
    return {
        "retrospective_holdout": holdout,
        "mandate": mandate, "estimates": full, "portfolios": portfolios,
        "baseline": base, "stresses": stresses,
        "signal": {
            "name": "12-month VTI performance relative to SGOV",
            "start": prior["date"], "price_cutoff": latest["date"],
            "available_utc": snapshot_ready, "relative_return": vti_relative,
            "reading": "VTI led SGOV" if vti_relative > 0 else "VTI did not lead SGOV",
            "use": "Context only. The signal does not change weights or authorize trades.",
            "sha256": digest, "sources": source["sources"],
        },
    }


if __name__ == "__main__":
    print(json.dumps(report(), indent=2))
