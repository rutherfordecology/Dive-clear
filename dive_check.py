#!/usr/bin/env python3
"""
Checks Gisborne dive conditions for today and the next few forecast days
against a personal rule, and sends one heads-up listing any days that pass -
by email, and/or as a phone push notification via ntfy.sh if NTFY_TOPIC is
set. Nothing is sent if no day passes. Meant to run on a schedule (see
.github/workflows/dive-check.yml) since this has no server of its own.

Forecast days are evaluated exactly like the dashboard does: wind and rain
windows roll forward and use forecast values for any days that haven't
happened yet, so the further ahead a day is, the less reliable its verdict.

Rule:
  - Swell threshold scales smoothly from 1.2 m (due south) to 2.0 m (due north)
    based on swell direction, rather than a hard S/SW/SE-vs-N/NE/NW split
  - Wind predominantly NW->N->NE for the last 5 days
    (implemented as: at least 4 of the last 5 days' dominant wind direction
    fell in that arc - this threshold is an assumption, not specified)
  - Less than 30 mm rain in the trailing 7 days

Data source: Open-Meteo marine + weather forecast APIs (free, no key needed).
"""

import datetime
import os
import smtplib
import sys
from email.mime.text import MIMEText

import requests

LAT, LON = -38.6623, 178.0176

# Today + 3 days ahead, matching FORECAST_DAYS in index.html.
FORECAST_DAYS = 4

MARINE_URL = (
    "https://marine-api.open-meteo.com/v1/marine"
    f"?latitude={LAT}&longitude={LON}"
    "&daily=swell_wave_height_max,swell_wave_direction_dominant"
    "&timezone=auto"
    f"&forecast_days={FORECAST_DAYS}"
)
WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    "&daily=winddirection_10m_dominant,precipitation_sum"
    "&timezone=auto&past_days=7"
    f"&forecast_days={FORECAST_DAYS}"
)


def compass(deg):
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return dirs[round(((deg % 360) + 360) % 360 / 22.5) % 16]


def is_favourable_wind_dir(deg):
    d = ((deg % 360) + 360) % 360
    return d >= 292.5 or d < 67.5  # NW -> N -> NE arc


def swell_threshold(deg):
    d = ((deg % 360) + 360) % 360
    # Smooth interpolation instead of a hard S/SW/SE-vs-N/NE/NW split: the threshold
    # rises from 1.2m (swell from due south, full impact on this coast) to 2.0m
    # (swell from due north, dampened impact), based on angular distance from north.
    dist_from_north = min(d, 360 - d)  # 0 at north, 180 at south
    leniency_frac = 1 - dist_from_north / 180  # 1 at north, 0 at south
    return 1.2 + (2.0 - 1.2) * leniency_frac


def evaluate_day(date, swell_h, swell_dir, wind_window, rain_window):
    favourable_count = sum(1 for d in wind_window if d is not None and is_favourable_wind_dir(d))
    wind_pass = favourable_count >= 4

    rain_total = sum(v for v in rain_window if v is not None)
    rain_pass = rain_total < 30

    if swell_h is not None and swell_dir is not None:
        threshold = swell_threshold(swell_dir)
        swell_pass = swell_h < threshold
        swell_score = max(0.0, min(1.0, 1 - swell_h / threshold)) * 100
    else:
        threshold, swell_pass, swell_score = None, False, 0.0

    # Suitability score: 0-100 per condition based on margin under threshold,
    # averaged with equal weighting (see README - this weighting is an assumption,
    # not based on research into which factor matters most for this coast).
    wind_score = (favourable_count / 5) * 100
    rain_score = max(0.0, min(1.0, 1 - rain_total / 30)) * 100
    overall_score = round((swell_score + wind_score + rain_score) / 3)

    return {
        "date": date,
        "swell_pass": swell_pass, "swell_h": swell_h, "swell_dir": swell_dir, "threshold": threshold,
        "wind_pass": wind_pass, "favourable_count": favourable_count, "wind_window": wind_window,
        "rain_pass": rain_pass, "rain_total": rain_total,
        "all_pass": swell_pass and wind_pass and rain_pass,
        "overall_score": overall_score,
    }


def fetch_conditions():
    """Returns one evaluated result per day: index 0 is today, then forecast days."""
    marine = requests.get(MARINE_URL, timeout=30).json()
    weather = requests.get(WEATHER_URL, timeout=30).json()

    w_time = weather["daily"]["time"]  # 7 past + today + (FORECAST_DAYS - 1) ahead
    wind_dir = weather["daily"]["winddirection_10m_dominant"]
    rain = weather["daily"]["precipitation_sum"]
    today_idx = len(w_time) - FORECAST_DAYS

    m_time = marine["daily"]["time"]  # today .. (FORECAST_DAYS - 1) ahead
    swell_h = marine["daily"]["swell_wave_height_max"]
    swell_dir = marine["daily"]["swell_wave_direction_dominant"]

    results = []
    for offset in range(min(FORECAST_DAYS, len(m_time))):
        i = today_idx + offset
        if m_time[offset] != w_time[i]:
            raise RuntimeError(f"Marine/weather dates out of step: {m_time[offset]} vs {w_time[i]}")
        # Wind: 5 days ending on (and including) this day.
        # Rain: 7 days ending on the day BEFORE this day. Same as index.html.
        results.append(evaluate_day(
            w_time[i], swell_h[offset], swell_dir[offset],
            wind_dir[max(0, i - 4):i + 1],
            rain[max(0, i - 7):i],
        ))
    return results


def day_label(r, offset):
    d = datetime.date.fromisoformat(r["date"])
    name = "Today" if offset == 0 else "Tomorrow" if offset == 1 else d.strftime("%A")
    return f"{name} ({d.strftime('%a %-d %b')})"


def build_day_section(r, offset):
    wind_chips = ", ".join(compass(d) for d in r["wind_window"] if d is not None)
    tag = "" if offset == 0 else " - forecast"
    return (
        f"{day_label(r, offset)}{tag}: suitability {r['overall_score']}/100\n"
        f"  Swell: {r['swell_h']:.1f} m from {compass(r['swell_dir'])} "
        f"(needed < {r['threshold']:.2f} m)\n"
        f"  Wind (5 days to this day): {r['favourable_count']}/5 days NW-N-NE ({wind_chips})\n"
        f"  Rain (7 days before): {r['rain_total']:.1f} mm (needed < 30 mm)\n"
    )


def build_message(results):
    """Returns (subject, body) if any day passes, else None."""
    good = [(o, r) for o, r in enumerate(results) if r["all_pass"]]
    if not good:
        return None

    ahead = [day_label(r, o).split(" (")[0] for o, r in good if o > 0]
    if good[0][0] == 0:
        subject = "Dive conditions good today - Gisborne"
        if ahead:
            subject += f" (forecast also good: {', '.join(ahead)})"
    else:
        subject = f"Dive forecast good for {', '.join(ahead)} - Gisborne"

    body = "Gisborne dive conditions pass the rule on:\n\n"
    body += "\n".join(build_day_section(r, o) for o, r in good)
    if any(o > 0 for o, _ in good):
        body += (
            "\nForecast days use predicted swell, wind and rain, so they can change. "
            "You'll get another message on the morning itself if it still looks good.\n"
        )
    return subject, body


def send_email(subject, body):
    user = os.environ["EMAIL_USER"]
    password = os.environ["EMAIL_PASS"]
    to_addr = os.environ["EMAIL_TO"]

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to_addr

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(user, password)
        smtp.sendmail(user, [to_addr], msg.as_string())


def send_ntfy(subject, body):
    topic = os.environ["NTFY_TOPIC"]
    requests.post(
        f"https://ntfy.sh/{topic}",
        data=body.encode("utf-8"),
        headers={"Title": subject},
        timeout=30,
    )


def main():
    results = fetch_conditions()
    for r in results:
        print(
            f"{r['date']}: swell={r['swell_pass']} wind={r['wind_pass']} "
            f"rain={r['rain_pass']} -> {'DIVE' if r['all_pass'] else 'no dive'} "
            f"(suitability {r['overall_score']}/100)"
        )

    msg = build_message(results)
    if msg is None:
        print("No day passes - no notification sent.")
        return
    subject, body = msg

    if os.environ.get("EMAIL_USER") and os.environ.get("EMAIL_PASS") and os.environ.get("EMAIL_TO"):
        send_email(subject, body)
        print("Email sent.")

    if os.environ.get("NTFY_TOPIC"):
        send_ntfy(subject, body)
        print("Push notification sent.")


if __name__ == "__main__":
    sys.exit(main())
