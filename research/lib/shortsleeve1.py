"""short-sleeve: `tsmom12` + a 10% SPY/QQQ downtrend short sleeve vs `tsmom12` + a 10% T-bill slot.

    uv run --with numpy python research/lib/shortsleeve1.py

Card: research/cards/short-sleeve.md (fixed before any number). One run: logs one `variant`
row (`short10@bills`) and one `baseline` row (`bill10@bills`) in tries.md, writes
results/short-sleeve.md. `tsmom12` is the gym's run of the logged baseline, re-scored with cash
at the T-bill (`log=False`); the sleeve is a paper series on adjusted closes (the gym cannot hold
shorts).
"""

from __future__ import annotations

import bisect
import csv
import fcntl
import math
from datetime import UTC, date, datetime, timedelta

import cash_interest
import common as c
import harness
import numpy as np
import stats

IDEA = "short-sleeve"
SLOT = 0.10  # share of the book in the slot
LEGS = {"SPY": 0.05, "QQQ": 0.05}  # fixed leg sizes, share of the book
BORROW = 0.01  # a year, on short notional
COST = 0.0005  # per side, on leg notional
FALL = 0.25
REBOUND = 365
CRASH = [
    ("2008", date(2008, 1, 1), date(2008, 12, 31)),
    ("2020-Q1", date(2020, 1, 1), date(2020, 3, 31)),
    ("2022", date(2022, 1, 1), date(2022, 12, 31)),
]
DRAWS, BLOCK, SEED = 2000, 20, 0


def short_signal(view: harness.View) -> harness.Weights:
    """Leg size (as a positive number) for each leg whose ETF's 12-month return is negative."""
    out = {}
    for s, w in LEGS.items():
        if c.eligible(view, s):
            r = c.trailing_logret(view, s, 365)
            if not math.isnan(r) and r < 0:
                out[s] = w
    return out


def calendar_closes(bars: list, days: list[date]) -> np.ndarray:
    """Last close on or before each calendar day."""
    bd = [b.date for b in bars]
    out = np.empty(len(days))
    for k, d in enumerate(days):
        i = bisect.bisect_right(bd, d) - 1
        out[k] = bars[max(i, 0)].close
    return out


def zigzag(px: np.ndarray, down: float, up: float) -> tuple[list[tuple[int, int]], int | None]:
    """insure-1's zigzag: confirmed (peak, trough) index pairs, and an unfinished fall's peak."""
    out: list[tuple[int, int]] = []
    falling, pk, tr = False, 0, 0
    for i in range(1, len(px)):
        if not falling:
            if px[i] > px[pk]:
                pk = i
            elif px[i] <= px[pk] * (1 - down):
                falling, tr = True, i
        else:
            if px[i] < px[tr]:
                tr = i
            elif px[i] >= px[tr] * (1 + up):
                out.append((pk, tr))
                falling, pk = False, i
    return out, (pk if falling else None)


def window_ret(r: np.ndarray, days: list[date], a: date, b: date) -> float:
    """Compounded return over calendar days a..b (r[k] is the return on days[k])."""
    i, j = bisect.bisect_left(days, a), bisect.bisect_right(days, b)
    return float(np.prod(1 + r[i:j]) - 1)


def log_row(variant: str, kind: str, r: np.ndarray, turnover: float, a: date, b: date) -> None:
    eq = np.cumprod(1 + r)
    mdd = float((1 - eq / np.maximum.accumulate(eq)).max())
    row = (
        f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {variant} | {kind} | train | {a} | {b} | "
        f"{stats.sharpe(r):.2f} | {eq[-1] - 1:+.1%} | {mdd:.1%} | {turnover:.2f} |\n"
    )
    with harness.TRIES.open("a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(row)


def save_curve(variant: str, days: list[date], r: np.ndarray) -> None:
    path = harness.DATA / "runs" / IDEA / f"{variant}.train.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    eq = np.cumprod(1 + r)
    with path.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["date", "equity_rel"])
        w.writerows((d.isoformat(), repr(float(e))) for d, e in zip(days, eq, strict=True))


def boot(a: np.ndarray, b: np.ndarray) -> tuple[float, float, float]:
    """Paired stationary bootstrap of Sharpe(a) - Sharpe(b): (d, one-sided p, SE)."""
    rng = np.random.default_rng(SEED)
    diffs = np.empty(DRAWS)
    for k in range(DRAWS):
        i = stats._stationary_indices(len(a), BLOCK, rng)
        diffs[k] = stats.sharpe(a[i]) - stats.sharpe(b[i])
    return stats.sharpe(a) - stats.sharpe(b), float((diffs <= 0).mean()), float(diffs.std())


def episodes(name: str, bars: list, days: list[date], dlog: np.ndarray) -> list[str]:
    """insure-1 decomposition of short10 - bill10 (log points) over one series' 25% falls."""
    first, last = days[0], days[-1]
    bars = [x for x in bars if first - timedelta(days=1) <= x.date <= last]
    px = np.array([x.close for x in bars])
    bd = [x.date for x in bars]
    cum = np.concatenate([[0.0], np.cumsum(dlog)])  # cum[k] = sum over days[0..k-1]

    def at(d: date) -> float:  # cumulative through calendar day d
        return float(cum[bisect.bisect_right(days, d)])

    pairs, open_pk = zigzag(px, FALL, FALL)
    out = [
        f"### {name}: 25% falls (zigzag on total-return closes)",
        "",
        "| Peak | Trough | Fall | I (fall) | B (rebound) | I + B |",
        "|---|---|---:|---:|---:|---:|",
    ]
    si = sb = 0.0
    pos = 0
    for j, (a, b) in enumerate(pairs):
        lim = bd[b] + timedelta(days=REBOUND)
        if j + 1 < len(pairs):
            lim = min(lim, bd[pairs[j + 1][0]])
        lim = min(lim, last)
        ins = at(bd[b]) - at(bd[a])
        reb = at(lim) - at(bd[b])
        si, sb, pos = si + ins, sb + reb, pos + (ins > 0)
        out.append(
            f"| {bd[a]} | {bd[b]} | {1 - px[b] / px[a]:.0%} | {ins:+.1f} | {reb:+.1f} | "
            f"{ins + reb:+.1f} |"
        )
    total = float(cum[-1])
    calm = total - si - sb
    prem = f"{-(sb + calm) / si:.2f}" if si > 0 else "n/a (sum I <= 0)"
    out += [
        "",
        f"Episodes {len(pairs)}, I > 0 in {pos}. Sum I {si:+.1f}, sum B {sb:+.1f}, calm C "
        f"{calm:+.1f}, total {total:+.1f} log points. **Premium P = -(B + C) / I: {prem}.**",
    ]
    if open_pk is not None:
        out.append(f"Unfinished fall at the end from peak {bd[open_pk]} (not scored).")
    return out + [""]


def main() -> None:
    six = c.ctx("six")
    tsm = c.go(
        "baselines", "tsmom12", c.weekly(c.slots(c.tsmom_signal)), six, "baseline", log=False
    )
    bdays, yields = cash_interest.bill_yield()
    r_tsm, rf = cash_interest.rescored(tsm, bdays, yields)
    days = tsm.days[1:]  # r[k] is the return on days[k]

    # Sleeve weights: the decision made on calendar day q-1, q = last SPY trading day before k
    # (decided after Friday's close, effective from the next trading day's close).
    decs = harness.decisions(
        c.weekly(short_signal), six.panel, harness.TRAIN_START, harness.TRAIN_END
    )
    wdec = {d.time.date(): d.weights for d in decs}
    first_dec = decs[0].time.date()
    tdays = [x.date for x in six.hist["SPY"]]
    pos = {s: np.zeros(len(days)) for s in LEGS}
    for k, d in enumerate(days):
        q = tdays[bisect.bisect_left(tdays, d) - 1]
        dd = q - timedelta(days=1)
        if dd >= first_dec:
            w = wdec[min(dd, harness.TRAIN_END)]
            for s in LEGS:
                pos[s][k] = w.get(s, 0.0)

    x = np.zeros(len(days))  # sleeve return over the bill slot, as a share of the book
    turn = 0.0
    legs_alone = {}
    for s in LEGS:
        px = calendar_closes(six.hist[s], [tsm.days[0], *days])
        ra = px[1:] / px[:-1] - 1
        p = pos[s]
        dw = np.abs(np.diff(np.concatenate([[0.0], p])))
        leg = p * (rf - BORROW / 365 - ra) - COST * dw
        legs_alone[s] = leg
        x += leg
        turn += float(dw.sum())
    years = len(days) / 365
    r_ctrl = (1 - SLOT) * r_tsm + SLOT * rf
    r_test = r_ctrl + x
    a, b = harness.TRAIN_START, harness.TRAIN_END
    turn_book = (1 - SLOT) * tsm.score.turnover + turn / years
    log_row("short10@bills", "variant", r_test, turn_book, a, b)
    log_row("bill10@bills", "baseline", r_ctrl, (1 - SLOT) * tsm.score.turnover, a, b)
    save_curve("short10@bills", days, r_test)
    save_curve("bill10@bills", days, r_ctrl)

    ex_t, ex_c = r_test - rf, r_ctrl - rf
    d, p, se = boot(ex_t, ex_c)
    z = d / se if se > 0 else float("nan")

    def line(name: str, r: np.ndarray) -> str:
        e = r - rf
        return (
            f"| {name} | {stats.sharpe(e):.3f} | {stats.cagr(r):+.2%} | {stats.vol(r):.1%} | "
            f"{stats.max_drawdown(r):.1%} |"
        )

    out = [
        "# short-sleeve: `tsmom12` + 10% SPY/QQQ downtrend short vs + 10% T-bill slot",
        "",
        "Card `cards/short-sleeve.md`. Train window, decisions "
        f"{a}..{b}; returns on calendar days {days[0]}..{days[-1]}. Cash, slot, collateral and "
        "short proceeds earn the 13-week T-bill; borrow 1%/yr; 5 bps a side on leg trades; "
        f"mix reset to 90/10 daily. Average bill yield {rf.mean() * 365:.2%}.",
        "",
        "## Whole window",
        "",
        "| Book | Sharpe above bills | CAGR | Vol | Max DD |",
        "|---|---:|---:|---:|---:|",
        line("`bill10` (control)", r_ctrl),
        line("`short10` (test)", r_test),
        line("`tsmom12` (cash at bills, for reference)", r_tsm),
        "",
        f"**Sharpe above bills, `short10` - `bill10`: d = {d:+.4f}, bootstrap SE {se:.4f}, "
        f"z = {z:+.2f}, one-sided p = {p:.4f}** (paired stationary bootstrap, {DRAWS} draws, "
        f"mean block {BLOCK} days). Family bar p < 0.00147; project bar z >= 4.65 (N_eff 433), "
        "Bonferroni p <= 1.2e-4.",
        "",
        f"Sleeve alone (over the bill slot, share of the book): {x.mean() * 365:+.3%} a year; "
        f"book turnover {turn_book:.2f}/yr (sleeve {turn / years:.2f}).",
    ]
    for s in LEGS:
        held = pos[s][pos[s] != 0]
        live = days.index(next(dd for dd in days if dd >= date(2000, 3, 11))) if s == "QQQ" else 0
        share = len(held) / (len(days) - live)
        out.append(
            f"- {s} leg: short {share:.0%} of the days it could be; contribution "
            f"{legs_alone[s].mean() * 365:+.3%} of the book a year, sum "
            f"{100 * np.log1p(legs_alone[s]).sum():+.1f} log points."
        )
    out += [
        "",
        "## Crash windows (total return)",
        "",
        "| Window | `bill10` | `short10` | Difference | SPY leg | QQQ leg |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    wins = CRASH + [(n, a_, b_) for n, a_, b_ in harness.STRESS[:4]]
    for n, wa, wb in wins:
        rc, rt = window_ret(r_ctrl, days, wa, wb), window_ret(r_test, days, wa, wb)
        ls = [window_ret(legs_alone[s], days, wa, wb) for s in LEGS]
        out.append(
            f"| {n} ({wa}..{wb}) | {rc:+.1%} | {rt:+.1%} | {rt - rc:+.1%} | "
            f"{ls[0]:+.1%} | {ls[1]:+.1%} |"
        )
    out += ["", "## Calendar years: worst and the sleeve's best and worst", ""]
    yrs = sorted({dd.year for dd in days})
    yc = {y: window_ret(r_ctrl, days, date(y, 1, 1), date(y, 12, 31)) for y in yrs}
    yt = {y: window_ret(r_test, days, date(y, 1, 1), date(y, 12, 31)) for y in yrs}
    wc, wt = min(yc, key=yc.__getitem__), min(yt, key=yt.__getitem__)
    out.append(f"- Worst year: `bill10` {wc} {yc[wc]:+.1%}; `short10` {wt} {yt[wt]:+.1%}.")
    diffs = sorted(yrs, key=lambda y: yt[y] - yc[y])
    out.append(
        "- Sleeve's worst years (difference): "
        + ", ".join(f"{y} {yt[y] - yc[y]:+.1%}" for y in diffs[:5])
    )
    out.append(
        "- Sleeve's best years (difference): "
        + ", ".join(f"{y} {yt[y] - yc[y]:+.1%}" for y in diffs[::-1][:5])
    )
    out.append(f"- Years the sleeve added: {sum(yt[y] > yc[y] for y in yrs)} of {len(yrs)}.")
    out += ["", "## By era: Sharpe above bills", "", "| Era | `bill10` | `short10` | d |"]
    out += ["|---|---:|---:|---:|"]
    for n, ea, eb in harness.ERAS[2:]:
        i, j = bisect.bisect_left(days, ea), bisect.bisect_right(days, eb)
        sc, st = stats.sharpe(ex_c[i:j]), stats.sharpe(ex_t[i:j])
        out.append(f"| {n} | {sc:.2f} | {st:.2f} | {st - sc:+.3f} |")
    dlog = 100 * (np.log1p(r_test) - np.log1p(r_ctrl))
    out += ["", "## Insurance, insure-1 style (log points of `short10` - `bill10`)", ""]
    out += episodes("SPY (US market, primary)", six.hist["SPY"], days, dlog)
    out += episodes("QQQ (second series)", six.hist["QQQ"], days, dlog)
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
