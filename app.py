"""Streamlit committee view for the frozen Project 2 mandate."""
import numpy as np
import streamlit as st

from decision import report
from portfolio import search

st.set_page_config(page_title="Portfolio mandate review", layout="wide")
st.title("Portfolio mandate review")
st.warning("Recommendation · Reject adoption for now. Authorize 0% for this process.")

try:
    evidence = report()
except (OSError, ValueError, KeyError) as error:
    st.error(f"Review stopped. {error}")
    st.stop()

mandate = evidence["mandate"]
estimates = evidence["estimates"]
floor = mandate["objective_annual_decimal"]
reserve = mandate["reserve_minimum"]
st.caption(f"Frozen snapshot ending {estimates['price_end']} · {estimates['observations']} monthly returns")
st.markdown(
    f"**Seven-year mandate.** Minimize estimated annual volatility. Require at least "
    f"{floor:.1%} estimated annual return and {reserve:.0%} in SGOV. "
    "Use VTI, BND and SGOV, long-only and fully invested. "
    "Benchmark against 60% VTI and 40% BND."
)

comparison, stress, signal = st.tabs(["Portfolios", "Stress tests", "Signal and data card"])
with comparison:
    rows = []
    for name, case in evidence["portfolios"].items():
        rows.append({
            "Portfolio": name,
            **dict(zip(mandate["tickers"], [f"{w:.1%}" for w in case["weights"]])),
            "Annual return": f"{case['return']:.2%}", "Annual volatility": f"{case['volatility']:.2%}",
            "Verdict": case["verdict"], "Failed rules": ", ".join(case["failures"]) or "None",
        })
    st.dataframe(rows, hide_index=True)
    if evidence["baseline"] is None:
        st.error("Stop. No grid allocation satisfies the mandate.")
    st.caption("The constrained search uses 5-percentage-point increments. Baselines use their stated weights.")
with stress:
    rows = []
    for label, case in evidence["stresses"].items():
        result = case["result"]
        rows.append({
            "Scenario": label,
            "VTI / BND / SGOV": " / ".join(f"{w:.0%}" for w in result["weights"]) if result else "—",
            "Annual net return": f"{result['return']:.2%}" if result else "—",
            "Annual volatility": f"{result['volatility']:.2%}" if result else "—",
            "Verdict": "PASS" if result else "STOP · No feasible mix",
        })
    st.dataframe(rows, hide_index=True)
    st.subheader("Test a cost and reserve assumption")
    cost = st.slider("Incremental annual cost (basis points)", 0, 100, 0)
    minimum = st.slider("Minimum SGOV reserve (%)", 0, 100, int(reserve * 100))
    result = search(np.asarray(estimates["returns"]) - cost / 10000,
                    estimates["covariance"], mandate["reserve_eligible"], floor, minimum / 100)
    if result:
        weights = ", ".join(f"{ticker} {weight:.0%}" for ticker, weight in zip(mandate["tickers"], result["weights"]))
        st.success(f"PASS · {weights} · {result['return']:.2%} estimated net return")
    else:
        st.error("STOP · No grid allocation satisfies the return and reserve floors.")
with signal:
    card = evidence["signal"]
    st.metric(card["name"], f"{card['relative_return']:+.2%}")
    st.write(card["reading"])
    st.caption(card["use"])
    st.write(f"Price dates {card['start']} to {card['price_cutoff']}. Snapshot available {card['available_utc']}.")
    st.caption("Yahoo Finance adjusted closes. Provider adjustments may be revised. Archived download supports this availability date only.")
    for item in card["sources"]:
        st.link_button(f"{item['ticker']} price source", item["source"])
    st.code(card["sha256"], language=None)
