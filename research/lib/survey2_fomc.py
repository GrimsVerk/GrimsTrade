"""Parse the Federal Reserve's FOMC calendar pages (downloads: read as text only) into the list
of scheduled announcement days for `fomc-cycle` (research/cards/fomc-cycle.md).

    uv run python -I research/lib/survey2_fomc.py

Source: federalreserve.gov `monetarypolicy/fomchistorical{1994..2020}.htm` and
`monetarypolicy/fomccalendars.htm`, saved under `<cache_root>/downloads/survey-2/fomc/`.
Output: `<cache_root>/derived/survey-2/fomc.csv` with `day0` (the last day of each scheduled
meeting). Prints only counts and the first and last date.
"""

from __future__ import annotations

import csv
import html
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macro  # noqa: E402

FIRST, LAST = 1994, 2025
NAMES = ["January", "February", "March", "April", "May", "June", "July", "August"]
NAMES += ["September", "October", "November", "December"]
MONTHS = {m: i + 1 for i, m in enumerate(NAMES)}
# historical pages: "<h5 ...>January 29-30 Meeting - 2008</h5>"
HIST = re.compile(r"<h5[^>]*>([^<]*)</h5>")
# "March 18", "January 29-30", "April/May 30-1", "June 30-July 1", then an optional note
HEAD = re.compile(r"^(\w+)(?:/(\w+))? (\d+)(?:-(?:(\w+) )?(\d+))? +(\(\w+\) )?Meeting - (\d{4})$")
# current page: "2025 FOMC Meetings" then month/date cells
YEAR = re.compile(r"(\d{4}) FOMC Meetings")
CELL = re.compile(
    r"fomc-meeting__month[^>]*><strong>([^<]*)</strong>|fomc-meeting__date[^>]*>([^<]*)<"
)


def day0(m1: str, m2: str | None, d1: str, d2: str | None, year: int) -> date:
    """The meeting's last day: the second month (if the meeting spans two) and the last date."""
    name = m2 or m1
    month = next(v for k, v in MONTHS.items() if k == name or k[:3] == name)
    if m2 is None and d2 is not None and int(d2) < int(d1):
        raise ValueError(f"{m1} {d1}-{d2}")
    return date(year, month, int(d2 or d1))


def historical(text: str) -> list[date]:
    out = []
    for h in HIST.findall(text):
        m = HEAD.match(html.unescape(h).strip())
        if not m:
            continue
        m1, m2, d1, m3, d2, note, y = m.groups()
        if note == "(unscheduled) ":
            continue  # (cancelled) is kept: it was on the published calendar
        out.append(day0(m1, m2 or m3, d1, d2, int(y)))
    return out


def merge(days: list[date]) -> list[date]:
    """Two 'meetings' at most 3 days apart are one (2003-09-15/16): keep the later day."""
    out: list[date] = []
    for d in sorted(days):
        if out and (d - out[-1]).days <= 3:
            out[-1] = d
        else:
            out.append(d)
    return out


def current(text: str) -> list[date]:
    out = []
    parts = YEAR.split(text)
    for i in range(1, len(parts), 2):
        year, body = int(parts[i]), parts[i + 1]
        month: str | None = None
        for mo, dt in CELL.findall(body):
            if mo:
                month = html.unescape(mo).strip()
                continue
            dt = html.unescape(dt).strip()
            if month is None or "notation" in dt or "unscheduled" in dt.lower():
                continue
            m = re.match(r"^(\d+)(?:-(\d+))?\*?", dt)
            if not m:
                continue
            m1, _, m2 = month.partition("/")
            out.append(day0(m1, m2 or None, m.group(1), m.group(2), year))
            month = None
    return out


def main() -> None:
    src = macro.cache_root() / "downloads" / "survey-2" / "fomc"
    days: set[date] = set()
    for y in range(FIRST, 2021):
        days.update(historical((src / f"hist{y}.htm").read_text(errors="replace")))
    days.update(current((src / "calendars.htm").read_text(errors="replace")))
    keep = merge([d for d in days if FIRST <= d.year <= LAST])
    out = macro.cache_root() / "derived" / "survey-2"
    out.mkdir(parents=True, exist_ok=True)
    with (out / "fomc.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["day0"])
        w.writerows([[d.isoformat()] for d in keep])
    per = {y: sum(d.year == y for d in keep) for y in range(FIRST, LAST + 1)}
    odd = {y: n for y, n in per.items() if n != 8}
    print(f"{len(keep)} scheduled meetings, {keep[0]} .. {keep[-1]}; years without 8: {odd}")


if __name__ == "__main__":
    main()
