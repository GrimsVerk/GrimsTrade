"""uv run python research/lib/wide5_deeper.py
Step 3 of wide-5 (research/wide-5.md): where `extension-dose` gains or loses against
`tsmom12`. Descriptive only: the card's configurations rerun without `tries.md` rows."""

from __future__ import annotations

import math
from datetime import date, timedelta

import common as c
import idea_wide5_extension_dose as x
import numpy as np
import wide1 as w
import wide5_rules as r

YEARS = range(2003, 2026)


def year_ret(run: c.Run, y: int) -> float:
    rr = run.rets_between(date(y - 1, 12, 31), min(date(y, 12, 31), c.TRAIN_END))
    return float(np.prod(1 + rr) - 1) if len(rr) else math.nan


def main() -> None:
    six = c.ctx("six")
    twin = c.go("baselines", "tsmom12", c.weekly(c.slots(c.tsmom_signal)), six, "baseline",
                log=False)  # fmt: skip
    hi = c.go(x.IDEA, "ext-high", x.overlay("TLT", True), six, "variant", log=False)
    lo = c.go(x.IDEA, "ext-low", x.overlay("TLT", False), six, "robustness", log=False)

    cal, ds, cls = x.series("TLT")
    win: set[date] = set()  # calendar days whose return the high overlay touches
    for j, h in cls.items():
        if h and j >= 3 and j + 1 < len(cal):
            d = cal[j - 3]
            while d <= cal[j + 1]:
                win.add(d)
                d += timedelta(days=1)
    a, b = c.align(hi, twin)
    first = max(hi.days[0], twin.days[0])
    days = [first + timedelta(days=k + 1) for k in range(len(a))]
    inwin = np.array([d in win for d in days])
    year = np.array([d.year for d in days])

    out = ["# wide-5 step 3: where `extension-dose` gains or loses against `tsmom12`", ""]
    out += ["Descriptive; questions fixed in `wide-5.md` before this was computed. Returns in "
            "percentage points; window = calendar days from T-3 to T+1 of high months.",
            ""]  # fmt: skip
    out += ["| Year | tsmom12 | ext-high minus twin | ext-low minus twin | of which in windows | "
            "of which outside | TLT year |", "|---|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    tlt = six.hist["TLT"]
    tyr: dict[int, float] = {}
    for y in YEARS:
        cl = [bar.close for bar in tlt if bar.date.year == y]
        prev = [bar.close for bar in tlt if bar.date.year == y - 1]
        tyr[y] = (cl[-1] / prev[-1] - 1) if cl and prev else math.nan
        m = year == y
        dh = 100 * (year_ret(hi, y) - year_ret(twin, y))
        dl = 100 * (year_ret(lo, y) - year_ret(twin, y))
        inn = 100 * float((a - b)[m & inwin].sum())
        outn = 100 * float((a - b)[m & ~inwin].sum())
        out.append(f"| {y} | {100 * year_ret(twin, y):+.1f} | {dh:+.2f} | {dl:+.2f} | "
                   f"{inn:+.2f} | {outn:+.2f} | {100 * tyr[y]:+.1f} |")  # fmt: skip
    out += [""]

    # per-month event-study excess (the card's number) with the splits of question 3
    days_t = [bar.date for bar in tlt]
    idx = {d: i for i, d in enumerate(days_t)}
    opens = np.array([bar.open for bar in tlt])
    ev = [(cal[j], cls[j], idx[cal[j]], j) for j in sorted(cls)
          if cal[j] in idx and cal[j] >= x.FIRST and idx[cal[j]] >= 3]  # fmt: skip
    ex = r.open_excess(opens, [i - 3 for _, _, i, _ in ev], 4, 0) * 1e4
    idle_at: dict[date, float] = {}
    for dec in twin.decisions:
        idle_at[dec.time.date()] = 1.0 - sum(dec.weights.values())
    dec_days = sorted(idle_at)

    def idle(d: date) -> float:
        k = int(np.searchsorted([q.toordinal() for q in dec_days], d.toordinal(), "right")) - 1
        return idle_at[dec_days[k]] if k >= 0 else math.nan

    rows = [(d, h, float(e), tyr.get(d.year, math.nan), idle(cal[j - 4]))
            for (d, h, _, j), e in zip(ev, ex, strict=True) if not math.isnan(e)]  # fmt: skip
    splits = [
        ("all", lambda q: True),
        ("bond bull years (TLT year > 0)", lambda q: q[3] > 0),
        ("bond bear years (TLT year < 0)", lambda q: q[3] < 0),
        ("2003-2013", lambda q: q[0].year <= 2013),
        ("2014-2025", lambda q: q[0].year >= 2014),
        ("idle >= 25% at T-4", lambda q: q[4] >= 0.25),
        ("idle < 25% at T-4", lambda q: q[4] < 0.25),
    ]
    out += ["TLT excess over the last four sessions (open T-3 to open T+1, bps, t), high and low "
            "months by the rule's split:", ""]  # fmt: skip
    out += ["| Split | High n | High | Low n | Low | High minus low |",
            "|---|---:|---:|---:|---:|---:|"]  # fmt: skip
    for name, f in splits:
        sub = [q for q in rows if q[0].year >= 2003 and f(q)]
        hh = np.array([q[2] for q in sub if q[1]])
        ll = np.array([q[2] for q in sub if not q[1]])
        se = math.sqrt(hh.var(ddof=1) / len(hh) + ll.var(ddof=1) / len(ll))
        out.append(f"| {name} | {len(hh)} | {hh.mean():+.1f} ({w.tstat(hh):+.2f}) | {len(ll)} | "
                   f"{ll.mean():+.1f} ({w.tstat(ll):+.2f}) | {hh.mean() - ll.mean():+.1f} "
                   f"(t {(hh.mean() - ll.mean()) / se:+.2f}) |")  # fmt: skip
    out += [""]
    path = c.harness.RESEARCH / "results" / "wide-5-deeper.md"
    path.write_text("\n".join(out).rstrip() + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
