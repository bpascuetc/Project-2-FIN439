# Project 2 portfolio tool and Lab 20

This local candidate uses the VTI, BND and SGOV mandate Bernat confirmed on October 22, 2026. It carries forward the frozen Lab 15 price data. The final Project 2 repository and Week 12 must-fix list are pending confirmation.

With Python 3 and NumPy installed, run this one command from the repository root.

```bash
python3 run_decision.py
```

The result is printed to the terminal. Read the [saved output](docs/decision-output.json) directly on GitHub and compare it with the [decision memo](docs/decision-memo.md).

Decision numbers should match the memo to the displayed precision. The final digits of unrounded floats can vary across environments.

Install the full dependencies before running the tests or launching the interactive tool.

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest test_engine -v
python3 -m streamlit run app.py
```

In the app, keep **My fund prices** selected. Adjust one control and read **Current lowest-risk mix** for the allocation and reserve result, or the warning when the grid has no feasible mix. This is a tool check. The separate Lab 20 prediction must be written, committed and pushed before its run.

See the [Lab 20 record](docs/lab20.md) for validation, AI use, and the individual checkout.

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
