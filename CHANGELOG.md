# Changelog

## v1.13
- Add three new locations: Goat Island, Poor Knights, and Wellington (Taputeranga) - each with its own rule derived by comparing swell/wind/rain on days with a confirmed Research-Grade fish photo (at a no-take reserve, so photos = divers not anglers) against random days in the same period.
- Rules are now fully per-location: each site enables only the conditions that showed a real signal (Goat Island is swell-only; Poor Knights is swell+rain; Wellington is swell+wind), and the day cards, scoring, and Info panel all adapt to show only what's relevant.
- Reassessed the Gisborne rule the same way; kept it unchanged since only 14 usable dive-days were found (too few to responsibly recalibrate), though the trend was consistent with the existing rule.
- Info panel now shows a "Rule for [location]" and "How this rule was derived" section specific to whichever location is selected.

## v1.12
- History chart shows 7 days at a time on mobile-width screens (was 30, cramped and unreadable) instead of the desktop's 30. Labels show a bare day number when every column is labeled, to avoid overlap.

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
