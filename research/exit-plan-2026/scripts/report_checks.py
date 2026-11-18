"""Consistency checks and small derived numbers for report.md (report writer, 2026-11-18).

No data download. Inputs are numbers quoted in the lane notes:
- S&P 500 closing high of about 7,819 on 2026-10-06 (bt.md Part C)
- DEGIRO Euronext Amsterdam fee EUR 2 + EUR 1 handling, core selection EUR 0 + EUR 1 (park.md 2.5)

Run: python3 -I research/exit-plan-2026/scripts/report_checks.py
"""

from datetime import date, timedelta

OSLO_CLOSED_2026 = {date(2026, 12, 24), date(2026, 12, 25), date(2026, 12, 31)}


def weekdays() -> None:
    dates = {
        "S&P/Nasdaq high": date(2026, 10, 6),
        "OSEBX high": date(2026, 10, 30),
        "S&P -4.36% day": date(2026, 11, 5),
        "last US close used": date(2026, 11, 17),
        "report day / Oslo close used": date(2026, 11, 18),
        "Anthropic first trade (Nasdaq notice)": date(2026, 11, 19),
        "Faber month-end check": date(2026, 11, 30),
        "ECB meeting": date(2026, 12, 17),
        "planned fallback sale": date(2026, 12, 18),
        "latest safe fallback sale": date(2026, 12, 21),
        "settles (sale 18 Dec)": date(2026, 12, 22),
        "settles (sale 21 Dec)": date(2026, 12, 23),
        "Oslo closed": date(2026, 12, 24),
        "last sale settling in 2026": date(2026, 12, 28),
        "last Oslo trading day": date(2026, 12, 30),
        "Oslo closed (New Year's Eve)": date(2026, 12, 31),
        "settles (sale 30 Dec)": date(2027, 1, 4),
        "Trade Republic promo end": date(2027, 3, 1),
        "re-entry deadline (calendar)": date(2028, 12, 31),
        "re-entry deadline (last weekday)": date(2028, 12, 29),
    }
    for name, d in dates.items():
        print(f"{d.isoformat()} {d.strftime('%a')}  {name}")


def oslo_trading_days() -> None:
    """Trading-day index from day 0 = 2026-11-18 (weekends and Oslo holidays skipped)."""
    d, i = date(2026, 11, 18), 0
    out = {}
    while d <= date(2026, 12, 30):
        if d.weekday() < 5 and d not in OSLO_CLOSED_2026:
            out[d] = i
            i += 1
        d += timedelta(days=1)
    for k in (0, 5, 10, 11, 15, 20, 22, 28):
        day = next(x for x, j in out.items() if j == k)
        print(f"Oslo trading day {k:2d} = {day.isoformat()} {day.strftime('%a')}")


def fees() -> None:
    for n, fee in ((3, 3.0), (12, 3.0), (3, 1.0), (12, 1.0)):
        print(f"DEGIRO re-entry, {n:2d} buys x EUR {fee:.0f} = EUR {n * fee:.0f}")


def reentry_levels() -> None:
    high = 7819.0
    for dd in (0.08, 0.20, 0.30, 0.40):
        print(f"S&P 500 {dd:.0%} below the ~7,819 high = {high * (1 - dd):,.0f}")


if __name__ == "__main__":
    weekdays()
    oslo_trading_days()
    fees()
    reentry_levels()
