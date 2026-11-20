# Project 2 — Investment management application

**AI use.** I used OpenAI Codex to help build the Python app, reproduce portfolio calculations, test failure cases and draft documentation.

**Ownership and purpose.** The analysis and decision are mine. This project is for education and does not provide investment advice.

## Run the app

From the repository root with Python 3.12:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit. Compare the three portfolios, move the minimum SGOV reserve slider to 100% to check the stop condition, then open the signal and data card. The app uses bundled data and needs no credentials.

Run `python decision.py` to reproduce the [saved output](docs/decision-output.json). Compare numbers to displayed precision. The CSV feeds the estimator and optimizer in `portfolio.py`. `decision.py` applies the mandate and builds the diagnostics. `app.py` displays the results and calls the same optimizer for interactive stresses.

- [Decision memo](docs/decision-memo.md)
- [Validation and AI use](docs/validation-and-ai-use.md)

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
