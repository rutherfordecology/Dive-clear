# Dive Conditions

Checks dive conditions on the Gisborne, NZ coast against a personal rule (swell
height/direction, 5-day wind trend, trailing 7-day rain) using free Open-Meteo
data, for either of two locations: Gisborne/Wainui or Makorori (they're far
enough apart to fall in different Open-Meteo grid cells).

- **`index.html`** — standalone dashboard, fetches live data client-side. Open it
  directly or serve it via GitHub Pages. Shows a Dive/No-dive verdict plus a
  0-100 suitability score for today and the next 3 days, the full breakdown
  (including high/low tide times and heights), a scrollable chart of the
  suitability score back to October 2021 (when swell data for this coast
  starts) — 30 days at a time, hold an arrow to scroll faster, or use the
  double-arrow to jump a month at a time — and an Info dropdown with the rule,
  scoring method, and assumptions.
- **`dive_check.py`** — same rule in Python; sends a heads-up (email and/or a
  phone push notification via [ntfy.sh](https://ntfy.sh)) only on days that
  pass. Run it on a schedule since a static page can't notify you itself.
- **`.github/workflows/dive-check.yml`** — runs `dive_check.py` daily via GitHub
  Actions, for free.

## Setup for notifications

In this repo's Settings -> Secrets and variables -> Actions, add any of:

| Secret | Value |
|---|---|
| `EMAIL_USER` | Your Gmail address |
| `EMAIL_PASS` | A Gmail [app password](https://myaccount.google.com/apppasswords) (not your normal password) |
| `EMAIL_TO` | Where the email alert should be sent |
| `NTFY_TOPIC` | A private, hard-to-guess topic name (e.g. `gisborne-dive-x7q2m`) |

Email and push notifications are independent — set up either or both. Skip
`EMAIL_*` to only get push notifications, or skip `NTFY_TOPIC` to only get email.

For push notifications: install the [ntfy app](https://ntfy.sh/) (iOS/Android),
subscribe to the same topic name you put in `NTFY_TOPIC`, and you'll get a
phone notification whenever conditions pass. Anyone who knows your topic name
can send you a notification, so pick something unguessable.

The workflow runs daily at 17:30 UTC (~5:30am NZ) and can also be triggered
manually from the Actions tab.
