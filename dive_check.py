#!/usr/bin/env python3
"""
Checks today's Gisborne dive conditions against a personal rule and sends
a heads-up only on days that pass - by email, and/or as a phone push
notification via ntfy.sh if NTFY_TOPIC is set. Meant to run on a schedule
(see .github/workflows/dive-check.yml) since this has no server of its own.

Rule:
  - Swell threshold scales smoothly from 1.2 m (due south) to 2.0 m (due north)
    based on swell direction, rather than a hard S/SW/SE-vs-N/NE/NW split
  - Wind predominantly NW->N->NE for the last 5 days
    (implemented as: at least 4 of the last 5 days' dominant wind direction
    fell in that arc - this threshold is an assumption, not specified)
  - Less than 30 mm rain in the trailing 7 days

Data source: Open-Meteo marine + weather forecast APIs (free, no key needed).
"""

import os
import smtplib
import sys
from email.mime.text import MIMEText

import requests

LAT, LON = -38.6623, 178.0176

MARINE_URL = (
    "https://marine-api.open-meteo.com/v1/marine"
    f"?latitude={LAT}&longitude={LON}"
    "&daily=swell_wave_height_max,swell_wave_direction_dominant"
    "&timezone=auto&forecast_days=1"
)
WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    "&daily=winddirection_10m_dominant,precipitation_sum"
    "&timezone=auto&past_days=7&forecast_days=1"
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


def fetch_conditions():
    marine = requests.get(MARINE_URL, timeout=30).json()
    weather = requests.get(WEATHER_URL, timeout=30).json()

    w_time = weather["daily"]["time"]  # 8 days: 7 past + today
    wind_dir = weather["daily"]["winddirection_10m_dominant"]
    rain = weather["daily"]["precipitation_sum"]
    today_idx = len(w_time) - 1

    wind_window = wind_dir[max(0, today_idx - 4):today_idx + 1]
    favourable_count = sum(1 for d in wind_window if d is not None and is_favourable_wind_dir(d))
    wind_pass = favourable_count >= 4

    rain_window = rain[max(0, today_idx - 7):today_idx]
    rain_total = sum(v for v in rain_window if v is not None)
    rain_pass = rain_total < 30

    swell_h = marine["daily"]["swell_wave_height_max"][0]
    swell_dir = marine["daily"]["swell_wave_direction_dominant"][0]
    threshold = swell_threshold(swell_dir)
    swell_pass = swell_h is not None and swell_h < threshold

    # Suitability score: 0-100 per condition based on margin under threshold,
    # averaged with equal weighting (see README - this weighting is an assumption,
    # not based on research into which factor matters most for this coast).
    swell_score = max(0.0, min(1.0, 1 - swell_h / threshold)) * 100 if swell_h is not None else 0.0
    wind_score = (favourable_count / 5) * 100
    rain_score = max(0.0, min(1.0, 1 - rain_total / 30)) * 100
    overall_score = round((swell_score + wind_score + rain_score) / 3)

    return {
        "date": w_time[today_idx],
        "swell_pass": swell_pass, "swell_h": swell_h, "swell_dir": swell_dir, "threshold": threshold,
        "wind_pass": wind_pass, "favourable_count": favourable_count, "wind_window": wind_window,
        "rain_pass": rain_pass, "rain_total": rain_total,
        "all_pass": swell_pass and wind_pass and rain_pass,
        "overall_score": overall_score,
    }


def build_email_body(r):
    wind_chips = ", ".join(compass(d) for d in r["wind_window"])
    return (
        f"Gisborne dive conditions look good for {r['date']}! "
        f"Suitability score: {r['overall_score']}/100\n\n"
        f"Swell: {r['swell_h']:.1f} m from {compass(r['swell_dir'])} "
        f"(needed < {r['threshold']:.2f} m)\n"
        f"Wind (last 5 days): {r['favourable_count']}/5 days NW-N-NE ({wind_chips})\n"
        f"Rain (trailing 7 days): {r['rain_total']:.1f} mm (needed < 30 mm)\n"
    )


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
    r = fetch_conditions()
    print(
        f"{r['date']}: swell={r['swell_pass']} wind={r['wind_pass']} "
        f"rain={r['rain_pass']} -> {'DIVE' if r['all_pass'] else 'no dive'} "
        f"(suitability {r['overall_score']}/100)"
    )
    if not r["all_pass"]:
        print("Conditions don't pass - no notification sent.")
        return

    subject = f"Dive conditions good for {r['date']} - Gisborne"
    body = build_email_body(r)

    if os.environ.get("EMAIL_USER") and os.environ.get("EMAIL_PASS") and os.environ.get("EMAIL_TO"):
        send_email(subject, body)
        print("Email sent.")

    if os.environ.get("NTFY_TOPIC"):
        send_ntfy(subject, body)
        print("Push notification sent.")


if __name__ == "__main__":
    sys.exit(main())
