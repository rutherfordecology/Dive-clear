# Gisborne Dive Conditions

Checks Gisborne, NZ dive conditions against a personal rule (swell height/direction,
5-day wind trend, trailing 7-day rain) using free Open-Meteo data.

- **`index.html`** — standalone dashboard, fetches live data client-side. Open it
  directly or serve it via GitHub Pages. Shows a Dive/No-dive verdict for today,
  tomorrow and the day after, plus the full breakdown and an assumptions panel.
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
