# Validation and AI use

Codex helped write the app and documentation, reconcile results against Lab 20 and compute the following diagnostics. Bernat confirmed the earlier reject decision and discussion with Brandon. Bernat also explicitly accepted the final Project 2 recommendation to reject adoption for now and authorize 0% allocation.

## Evidence and highest-risk claim

- **Known answer.** The 60-return sample reproduces the Lab 20 30/0/70 allocation, 6.54% estimated annual return, 4.85% volatility and 72 feasible mixes. An AI-generated suggestion to require byte-for-byte reproduction was checked against Brandon's ZIP run. Three floats differed in their last digits while the decision matched. Use displayed precision.
- **Stress and failure.** The CLI and app share the same 5-point grid. The estimate, window, cost, reserve and combined cases are saved with full precision. The return and reserve floors remain enforced under stress. Changing the interactive reserve to 100% produced the expected stop.
- **Holdout.** The fixed 48/12 split estimates through September 2025 and evaluates 12 monthly returns through September 2026. The 35/0/65 training allocation earned 7.86% gross compounded with monthly rebalancing. No costs are deducted from this diagnostic. Source revisions may reach backward and the period is short. The result cannot settle seven-year suitability.
- **Cold run.** Brandon ran the Lab 20 ZIP's decision command in a NumPy-only sandbox and reproduced weights, verdicts and rounded values. Four Streamlit tests required the full dependencies, now specified in the README. Independent clean-clone and live control verification for this Project 2 revision are pending.
- **Source and timing.** The bundled CSV contains Yahoo Finance adjusted closes sampled at the final available session of each month. The date labels are calendar month ends. Missing or invalid price rows stop estimation. Source URLs, fields, retrieval timestamps and price hash are in [price_sources.json](../price_sources.json). Adjustments are provider-defined and can be revised. Review redistribution terms before publishing the snapshot. There are no credentials, client holdings or personally identifying input data in the CSV.
- **Signal data card.** Divide the 12-month VTI adjusted-close growth factor by the SGOV growth factor and subtract one. September 2025 through September 2026 produced +11.18%. The latest download timestamp on October 22, 2026 bounds the signal's evidenced availability. It has no mandate effect.

## Edition A and B boundary

Use the preserved Lab 20 candidate as the documented starting comparison for this revision. It tested the constrained mix, the recent window and a cost diagnostic. The current revision adds mandate verdicts for two baselines, the dated signal, more stress dimensions, a stop control and a chronological holdout. The reject decision persisted. This comparison does not establish the timing of a formal Edition A checkpoint.

## Locked Changed-Input Record

**Prediction locked before the run.** Codex verified the 35 bp prediction in the [pre-run GitHub commit](https://github.com/bpascuetc/Project-2-FIN439/commit/d7943403f0b8b3677397573eac616e1e417efc1b) before executing the changed setting. The prior Lab 20 90-month prediction remains in the Lab 20 record. The student's original text is preserved below.

```text
Project 2 – Stress-test prediction (written before running the Stress tests tab)
Exact change
Assumption changed: annual incremental cost
From 0 bps to 35 bps per year, subtracted from each fund's estimated return
Held fixed: SGOV minimum reserve = 3%, 60-month sample through Sep 2026, 5-pp grid, long-only, fully invested, 6.5% return floor
Reasoning
Back-solving the three published portfolios (equal weight 5.48%, 60/40 7.71%, selected 30/0/70 6.54%) gives implied annual returns of roughly:
Fund	Implied est. annual return
VTI	~13.11%
BND	~-0.40%
SGOV	~3.72%
Because the portfolio is fully invested, a uniform 35 bp cost lowers every candidate's return by exactly 0.35 pp.
30/0/70: 6.54% - 0.35% = 6.19% -> fails the 6.5% floor (it already fails at 5 bps, since the baseline margin is only ~4 bps)
35/0/65: 7.01% - 0.35% = 6.66% -> clears the floor
BND has a negative estimated return, so adding it lowers return. Moving SGOV into BND is also likely to raise volatility. I don't expect BND to enter.
Prediction
Result: PASS
Predicted weights: 35% VTI / 0% BND / 65% SGOV. VTI goes up 5 pp and SGOV goes down 5 pp compared with 30/0/70.
Predicted estimated net return: about 6.66%, up about 12 bps from 6.54%
Predicted volatility: up from 4.85% to roughly 5.5–5.7%, because more of the portfolio is in VTI
(For reference: under my back-solve, the search should not STOP until cost exceeds about 1,230 bps, when even 97/0/3 falls below 6.5%.)
Would this change my committee recommendation?
No. I would still recommend rejecting adoption and allocating 0% to this process. A realistic 35 bp cost forces the selected mix to move, which is more evidence that the selection is fragile. A cost of only 5 bps is enough to make the original 30/0/70 fail, so the "selected portfolio" depends on assumptions inside normal estimation and cost noise.
Actual result (fill in after running the Stress tests tab)
PASS / STOP:
New weights (VTI / BND / SGOV):
Estimated net return:
Estimated volatility:
Exact STOP message (if any):
Comparison
Against my prediction:
Against original 30% / 0% / 70%:
```

### Actual result

- **Run:** November 20, 2026. Codex used Streamlit AppTest to set **Incremental annual cost** to **35 bp** in **Stress tests**, with **Minimum SGOV reserve** at **3%** and the original 60-month inputs. The app reported **PASS · VTI 35%, BND 0%, SGOV 65% · 6.66% estimated net return**.
- **Model output:** Estimated annual volatility was **5.64%**. **64 of 231** grid mixes qualified. Volatility comes from the model output. The interactive result displays the weights and net return. [Saved result](locked-35bp-result.json)
- **Against the prediction:** The PASS verdict, weights and rounded net return matched. Volatility fell within the predicted 5.5–5.7% range.
- **Against the original portfolio:** At the same 35 bp cost, the original 30/0/70 mix earns about **6.19%** and fails the **6.50%** floor. Reoptimization shifts **5 percentage points** from SGOV to VTI. Relative to the zero-cost baseline, the new mix's estimated net return increases about **12 bp** and estimated volatility increases **0.79 percentage points**. The higher return reflects the new allocation.
- **Decision effect:** The result supports keeping the approved recommendation to **reject adoption for now and authorize 0%**. The 5-point move is within the proposed 10-point limit for this test. The separate estimate and window stresses still moved VTI by 15 points.
- **Scope:** The original 1,230 bp comment was outside this test. The 97/0/3 mix is outside the 5-point grid, and the app's cost slider ends at 100 bp.

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
