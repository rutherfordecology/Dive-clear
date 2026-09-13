# Changelog

## v1.11
- Add a Morning/Midday/Afternoon swell breakdown per day, using hourly swell data instead of just the daily max/dominant-direction figures.

## v1.10
- Fix history chart date labels being clipped by `overflow: hidden` on very narrow per-day columns.

## v1.9
- Add a visible version number to the dashboard footer.

## v1.8
- Lighten and re-blue the color palette (the first pass read as near-black rather than gunmetal blue).

## v1.7
- Add a location switcher: "Gisborne / Wainui" and "Makorori" tabs, persisted via localStorage.
- History chart anchored to Oct 2021 (start of available swell data) instead of a rolling 2-year window.
- Add double-arrow buttons to jump the history chart a month at a time (hold to accelerate).
- Recolor to a gunmetal/clear-blue theme.
- Move the verdict badge next to the day label; fix the day-card grid to never split 3+1 or 2+2.

## v1.6
- Extend the forecast from today+2 to today+3 days ahead.
- Add high/low tide times and heights per day, derived from Open-Meteo's modeled sea level curve.
- Move the suitability history chart above the info panels.
- Merge the Rule, Suitability score, and Assumptions sections into one "Info" dropdown.
- Drop the per-day "(need < Xmm)" / "(need < X.XXm)" threshold text from the cards.

## v1.5
- Replace the hard S/SW/SE-vs-N/NE/NW swell threshold split with a smooth curve based on angular distance from north.

## v1.4
- Add a scrollable chart of the suitability score over the last 2 years (30 days visible at a time).

## v1.3
- Add a 0-100 suitability score alongside the pass/fail verdict.

## v1.2
- Only attempt to send email when all three EMAIL_* secrets are set, to avoid a crash on partial config.

## v1.1
- Add optional ntfy.sh push notifications alongside email.

## v1.0
- Initial dashboard, Python checker script, and GitHub Actions workflow.
