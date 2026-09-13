# Dive Conditions

Checks dive/snorkel conditions against a rule using free Open-Meteo data, for
nine NZ locations:

| Location | Rule | Basis |
|---|---|---|
| Gisborne / Wainui | Swell 1.2-2.0m (directional), wind (NW-N-NE), rain | Your own calibrated rule |
| Makorori | Same as Gisborne | Borrowed (not enough local data to calibrate its own) |
| Goat Island | Swell < 0.6m, wind (SW-centred, not NW-N-NE) | Derived from iNaturalist photo patterns |
| Poor Knights | Swell < 1.6m, rain < 15mm/7d | Derived from iNaturalist photo patterns |
| Wellington (Taputeranga) | Swell < 1.4m, wind (NW-N-NE), rain < 25mm/7d | Derived from iNaturalist photo patterns |
| Porirua | Swell < 0.9m, wind (SE-centred) | Derived from iNaturalist photo patterns |
| Bay of Islands | Rain < 25mm/7d only | Derived, smaller sample - more tentative |
| Kapiti | Swell < 0.8m only | Derived, strongest single-factor result found |
| Torbay | Swell < 0.25m only | Derived, smaller sample - more tentative |

The seven "derived" locations were calibrated by finding days where one
observer photographed 3+ distinct fish species in the area — strong
behavioural evidence of a real dive, regardless of species or local fishing
rules (this works even outside a no-take marine reserve, since anglers rarely
photograph a diverse haul) — and comparing swell/wind/rain on those days
against random days in the same period. Not every condition applies at every
site: only the ones that showed a real, consistent difference are included, so
some locations skip swell, wind, or rain entirely. Wind isn't assumed to
always favour NW-N-NE either: each site's favourable direction (if any) was
found by breaking wind direction into 16, 8, and 4 compass sectors and
checking whether a consistent favoured direction held across all three
resolutions - Goat Island and Porirua both turned out to favour a different,
site-specific direction. Porirua, Bay of Islands, Kapiti, and Torbay were
found via a national scan (binning tens of thousands of NZ fish photos into a
grid and ranking cells by the same 3+-species-day signal) rather than being
picked by name; Waikawau, Kaikoura, New Plymouth, and Dunedin were checked the
same way but didn't have enough data to trust a derived rule.

- **`index.html`** — standalone dashboard, fetches live data client-side. Open it
  directly or serve it via GitHub Pages. Location tabs at the top (your choice
  persists via localStorage); each shows a Dive/No-dive verdict plus a 0-100
  suitability score for today and the next 3 days, the full breakdown for
  whichever conditions apply at that site (including high/low tide times and
  heights), a scrollable chart of the suitability score back to October 2021
  (when swell data starts) — 30 days at a time on desktop, 7 on mobile, hold an
  arrow to scroll faster or use the double-arrow to jump a month at a time —
  and an Info dropdown with that site's specific rule, how it was derived,
  scoring method, and assumptions.
- **`dive_check.py`** — same rule in Python, for Gisborne only; sends a heads-up
  (email and/or a phone push notification via [ntfy.sh](https://ntfy.sh)) only
  on days that pass. Run it on a schedule since a static page can't notify you
  itself.
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
