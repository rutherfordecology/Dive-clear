# Changelog

## v1.20
- Fix the default map view being an unreadable wall of overlapping name tags where sites cluster tightly (mainly around Auckland/Northland). Labels are now hidden whenever another dot sits within 36px of them on screen, showing only dots by default, and reappear progressively as zooming spreads the cluster apart. The currently selected site's tag always stays visible regardless of crowding.

## v1.19
- The map is now open by default instead of hidden behind a button, with a minimise control to collapse it when you don't need it.
- Location names are now tags directly on the map next to each site's dot, instead of a separate row of buttons above it.
- The map is now zoomable and pannable: scroll/pinch to zoom (anchored under the cursor or between your fingers), drag to pan, double-click to step in, and +/-/reset buttons for a mouse-free option. Zooming in is what makes the tightly-clustered sites (there are several close together around Auckland/Northland) readable, since name tags stay a constant on-screen size while zooming spreads the dots further apart.

## v1.18
- Add a simple map view: a "Map" button next to the title shows an outline of NZ with every location plotted as a dot, the current selection highlighted. Click any dot to switch to that location, same as the tabs above it.

## v1.17
- Add **Ohinau Island** (swell + rain), found by directly testing an idea: comparing conditions on confirmed dive days against every other kind of day at the same spot, rather than against random days nationally. Swell showed the strongest single-factor result checked so far (Cohen's d -1.15).
- Ran a full national sweep of every remaining fish-photo cluster in the country (not just individually-picked candidates) and derived rules for every one with enough data and a real, consistent signal. Added eight more: **Tutukaka** (rain only), **Kaikoura** (swell - previously left out, now included after a cleaner re-check), **Matauri Bay** (swell + rain), **Stewart Island** (swell), **Akaroa** (swell, tentative), **Mangawhai** (swell - the site originally suggested as a data-rich example), **Far North** (swell + rain, smallest sample in the app so most tentative), and **Waiheke Island** (swell + rain) and **Great Barrier Island** (swell, tentative).
- Checked but left out: Dunedin, two further Northland clusters, a second Banks Peninsula cluster, an Auckland-suburbs cluster, Fiordland (swell went the wrong direction - likely because the local swell reading doesn't reflect sheltered fiord conditions), and New Plymouth - each either too thin on data or without a clean, consistent signal.
- The app now covers 19 locations in total.

## v1.16
- Add two new locations found via the national grid scan and re-checked with the reliable one-observer-3+-species method: **Kapiti** (swell only, under ~0.8m - the strongest single-factor result seen in this whole project) and **Torbay** (swell only, under ~0.25m - a sheltered inner-Hauraki-Gulf spot similar to Goat Island, smaller sample so treated as more tentative).
- Checked but skipped Dunedin: too few qualifying multi-species days (19) to trust a derived rule.
- History timeline now extends into the forecast days already shown on the day cards, drawn with a hashed, translucent fill so forecast bars are visually distinct from confirmed history.
- Info panel trimmed down to just the rule list for the selected location - dropped the "how this rule was derived" and assumptions narrative.

## v1.15
- Add a national site-discovery scan: binned all ~22,000 NZ Research-Grade fish photos since Oct 2021 into an ~11km grid and ranked cells by the same "3+ species by one observer in one day" quality signal used for rule derivation, to find genuine hotspots rather than guessing town names.
- Added two new locations found this way: **Porirua** (swell + wind, ranked higher than Poor Knights had) and **Bay of Islands** (rain only, smaller sample - noted as more tentative).
- Checked but didn't add: Waikawau, Kaikoura, New Plymouth - each had either too little total data or too few qualifying multi-species days to trust a derived rule.
- Swell can now be disabled per-location too (previously only wind/rain could be), for sites like Bay of Islands where no reliable swell threshold could be derived - the day cards, scoring, and rule summary text all adapt automatically.

## v1.14
- Re-derived the Goat Island, Poor Knights, and Wellington rules using a stronger "visited" proxy: days where one observer photographed 3+ distinct fish species (behavioural evidence of a real dive, regardless of species or reserve status) vs random days. Every effect got stronger than the previous single-photo method, and surfaced a real rain signal at Wellington that the old method missed entirely.
- Wind rules are no longer tied to a single fixed NW-N-NE arc: added a generalizable favourable-direction system (any centre direction + width). Empirically found Goat Island's favourable wind is centred on SW, not NW-N-NE - confirmed by breaking wind direction into 16, then 8, then 4 compass sectors and checking the result held at every resolution. This fits the same "favourable wind blows offshore" pattern as every other site, just a different compass direction because Goat Island faces NE.
- Poor Knights' wind signal stayed inconsistent across sector resolutions (a fully offshore island with no single sheltering coastline), so it's left without a wind rule.
- Updated thresholds: Poor Knights rain tightened to 15mm/7d; Wellington swell tightened to 1.4m and gained a 25mm/7d rain condition.

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
