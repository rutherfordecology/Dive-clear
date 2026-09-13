# Gisborne Dive Conditions

Checks Gisborne, NZ dive conditions against a personal rule (swell height/direction,
5-day wind trend, trailing 7-day rain) using free Open-Meteo data.

- **`index.html`** — standalone dashboard, fetches live data client-side. Open it
  directly or serve it via GitHub Pages. Shows a Dive/No-dive verdict for today,
  tomorrow and the day after, plus the full breakdown and an assumptions panel.
- **`dive_check.py`** — same rule in Python; emails you (Gmail SMTP) only on days
  that pass. Run it on a schedule since a static page can't send email itself.
- **`.github/workflows/dive-check.yml`** — runs `dive_check.py` daily via GitHub
  Actions, for free.

## Setup for the daily email

In this repo's Settings -> Secrets and variables -> Actions, add:

| Secret | Value |
|---|---|
| `EMAIL_USER` | Your Gmail address |
| `EMAIL_PASS` | A Gmail [app password](https://myaccount.google.com/apppasswords) (not your normal password) |
| `EMAIL_TO` | Where the alert should be sent |

The workflow runs daily at 17:30 UTC (~5:30am NZ) and can also be triggered
manually from the Actions tab.
