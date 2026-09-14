# Dive Conditions

Checks dive/snorkel conditions against a rule using free Open-Meteo data, for
19 NZ locations:

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
| Ohinau Island | Swell < 1.0m, rain < 25mm/7d | Derived, one of the strongest results found |
| Tutukaka | Rain < 30mm/7d only | Derived from a full national cluster sweep |
| Kaikoura | Swell < 1.5m only | Derived - previously left out, now included |
| Matauri Bay | Swell < 1.4m, rain < 25mm/7d | Derived from a full national cluster sweep |
| Stewart Island | Swell < 0.7m only | Derived from a full national cluster sweep |
| Akaroa | Swell < 1.6m only | Derived, smaller sample - more tentative |
| Mangawhai | Swell < 0.6m only | Derived, strongest single-factor result found |
| Far North | Swell < 1.5m, rain < 20mm/7d | Derived, smallest sample in the app - most tentative |
| Waiheke Island | Swell < 0.3m, rain < 20mm/7d | Derived from a full national cluster sweep |
| Great Barrier Island | Swell < 0.9m only | Derived, smaller sample - more tentative |

The 17 "derived" locations were calibrated by finding days where one
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
site-specific direction (a few of the newer sites show signs of the same
pattern but haven't had the sector check run yet, so their wind rule is left
out for now rather than guessed at).

Porirua, Bay of Islands, Kapiti, Torbay, Tutukaka, Matauri Bay, Stewart
Island, Akaroa, Mangawhai, Far North, Waiheke Island, and Great Barrier Island
were all found via a national scan (binning fish photos nationwide into a grid
and ranking cells by the same 3+-species-day signal) rather than being picked
by name. Ohinau Island came from testing a different idea directly: comparing
confirmed dive days against every other day at the same spot, rather than
against random days nationally. Checked but left out for having too little
data or no clean, consistent signal: Waikawau, New Plymouth, Dunedin, a couple
of further Northland clusters, a second Banks Peninsula cluster near
Lyttelton, an Auckland-suburbs cluster, and Fiordland (where swell went the
wrong direction, most likely because a single offshore swell reading doesn't
reflect conditions inside a sheltered fiord).

- **`index.html`** — standalone dashboard, fetches live data client-side. Open it
  directly or serve it via GitHub Pages. Choose a location from the zoomable,
  pannable map at the top (name tags next to each site's dot; scroll/pinch to
  zoom, drag to pan) - your choice persists via localStorage, and the map can
  be minimised once you've settled on a usual spot. Each location shows a
  Dive/No-dive verdict plus a 0-100 suitability score for today and
  the next 3 days, the full breakdown for whichever conditions apply at that
  site (including high/low tide times and heights), a scrollable chart of the
  suitability score back to October 2021 (when swell data starts) - extending
  into the forecast days with a hashed fill - 30 days at a time on desktop, 7
  on mobile, hold an arrow to scroll faster or use the double-arrow to jump a
  month at a time — and an Info dropdown with that site's specific rule.
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
