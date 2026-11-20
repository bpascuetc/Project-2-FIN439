# Project 2 — Committee decision memo

**AI use.** I used OpenAI Codex to help build the app, reproduce the calculations, check risk and sensitivity, and draft this memo.

**Ownership and purpose.** The analysis and decision are mine. This project is for education and does not provide investment advice.

## Committee decision

**Reject adoption for now. Authorize 0% for this process.** The model found a feasible mix, but its baseline return cushion is only about 4 basis points and its equity weight changes by 15 percentage points under plausible estimate or window changes. The committee should retain its existing policy pending validation. The historical stress results imply a research range of 15–45% VTI, 0% BND and 55–85% SGOV. The proposed implementation allocation is 0%.

## Mandate and comparison

The student-confirmed Project 2 mandate uses the committee decision framework from Lab 13 and the seven-year VTI/BND/SGOV policy confirmed on October 22. It minimizes annualized volatility subject to a 6.5% estimated annual return floor, a 3% minimum SGOV reserve, long-only holdings and full investment. The 60/40 diagnostic benchmark has no reserve sleeve by construction. The archive contains the separate Meridian case and its constraints.

| Portfolio | VTI / BND / SGOV | Annual return | Annual volatility | Verdict |
| --- | --- | ---: | ---: | --- |
| Equal weight | ⅓ / ⅓ / ⅓ | 5.48% | 6.92% | Fail, return floor |
| 60/40 benchmark | 60% / 40% / 0% | 7.71% | 11.38% | Fail, reserve floor |
| Constrained | 30% / 0% / 70% | 6.54% | 4.85% | Pass |

Annual estimates use 12 times the arithmetic monthly mean and 12 times the sample monthly covariance. The search considers 231 allocations in 5-point increments, of which 72 pass. The frozen snapshot ends September 30, 2026.

## What changes the decision

A one-point reduction in all estimated fund returns selects 45% VTI. The last 36 months select 15% VTI. A flat 25 bp annual cost selects 35% VTI. The 50% reserve stress leaves the baseline intact, while the combined shorter window, 125 bp total drag and 50% reserve selects 20% VTI. A 100% reserve requirement leaves no allocation meeting the return floor and stops the process. A frozen 12-month retrospective holdout returned 7.86% gross at monthly rebalanced 35/0/65 weights. It covers one year from a revised-price snapshot and provides limited evidence for a seven-year policy.

Review quarterly. Reopen the decision if updated data support the 6.5% floor after documented implementation costs, the reserve stays compliant, and the committee agrees on acceptable weight movement across plausible stresses. As a proposed review threshold, require at most 10 percentage points of movement in any sleeve. Pause on corrupt or missing source data, any unapproved mandate change or absence of a feasible mix. The relative VTI–SGOV signal is context only and has no execution authority.

See the [saved results](decision-output.json) and [validation record](validation-and-ai-use.md).

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
