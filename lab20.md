# Lab 20 — Project 2 readiness

## Readiness and validation

| Manifest item | Local evidence | Remaining evidence |
| --- | --- | --- |
| Tool | app.py uses the same grid search as the command-line runner | Partner control check |
| Repository | README lists the one command | Actual Project 2 GitHub URL and partner access |
| Visible output | decision-output.json saves baseline, recent window and existing cost stress | GitHub file URL |
| Decision memo | decision-memo.md uses the same inputs and outputs | Confirm this is the current Project 2 decision |
| Validation and AI use | Local reproduction and tests, below | Student-authored Locked Changed-Input Record |
| Videos 1–3 and transcripts | Project 2 files and links pending | Verify each link and its content |

OpenAI Codex prepared this local candidate from the saved Lab 15 portfolio model and drafted the record and memo. The baseline, mandate check and historical 25 bp cost diagnostic were reproduced locally. The cost stress belongs to the existing validation and is separate from the Lab 20 prediction exercise. The Week 12 must-fix list and the due date shown in the Brightspace assignment header are pending.

All eight tests passed locally with the full dependencies. Independent environments should reproduce the decision numbers to the displayed precision.

## Partner cold run

Brandon reported a sandbox run from the emailed ZIP on November 17 using NumPy 2.5.3. GitHub commit and clone-to-result timing are pending.

- Command and elapsed time — `python3 run_decision.py`, about 0.07 seconds for the command.
- Result location — terminal output, checked against `docs/decision-output.json` and the decision memo.
- Result — clean exit. The mandate verdict, allocation weights and rounded numbers matched. Three unrounded floats differed in their final digits.
- Separate test finding — four Streamlit tests failed in the NumPy-only environment with `ModuleNotFoundError: No module named 'streamlit'`.
- App control — pending a partner run with Streamlit installed.

## Locked Changed-Input Record

Bernat’s original prediction from the conversation: “ill choose 90 months now, and i predic that the anual return will decrease to about 6.00”

**AI-assisted completion.** I predict that increasing the estimation window from 60 to 90 monthly returns will lower the estimated annual return of my existing 30% VTI / 0% BND / 70% SGOV allocation from 6.54% to about 6.00%. With the 6.5% floor fixed, I expect that mix to fail the return check. If the optimizer finds another feasible mix, I expect it to take more equity risk to clear the floor. My decision remains **reject adoption for now**. The equity-risk prediction and decision implication are AI-assisted additions. The 36- and 60-month results were discussed before this prediction.

Saved locally before reproducing the baseline. The course’s AI-closed prediction and pre-run GitHub commit and push are unverified.

**Run outcome.** The [60-month rerun](window-60-baseline.json) reproduced the 30% VTI / 0% BND / 70% SGOV allocation, 6.54% estimated annual return, 4.85% estimated annual volatility and a passing baseline mandate check. The 90-month case is blocked by data availability. A window ending September 2026 needs prices from March 2019 through September 2026, while SGOV launched May 26, 2020. At most 76 monthly returns can span those post-launch month-end dates. The 6.00% prediction remains untested and the rerun provides no new basis to reverse the decision. [iShares SGOV fund page](https://www.ishares.com/us/products/314116/ishares-0-3-month-Treasury-bond-etf)

## Explain the code

Bernat confirmed that he completed the discussion with Brandon. The exact code question and answer were not supplied.

## Fix and rerun

The README now gives the full dependency install and the test command, and sets the expected precision for reproduction. The decision command itself ran cleanly in Brandon’s environment. GitHub fix commit and partner rerun are pending.

## Decision and reflection

Bernat confirmed the decision: **Reject adoption for now. Reconsider when fresh validation under the same mandate supports a mix with defensible allocation sensitivity and estimated net performance.**

Bernat confirmed he covered the discussion items with Brandon. The specific reflection wording was not supplied.

## Checkout

Brightspace → Quizzes → Lab 20. Use actual GitHub links to this record, the README, decision output and memo, and relevant Python or evidence files. Quiz attempt, links and submission are pending.

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
