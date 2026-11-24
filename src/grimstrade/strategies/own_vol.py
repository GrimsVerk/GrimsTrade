"""Own-vol target 70%: `tsmom12` sized by its own recent swings, in the no-look-ahead form of
research lane risk-menu-3 (PR #110, `research/risk-menu.md`, `research/lib/riskmenu3_run.py`).
Owner decision C2 (`research/owner-decisions.md`): keep the presets, add this one paper book.

The rule, as risk-menu-3 ran it:
1. `tsmom12`: every asset with a year of bars (365 for crypto, 252 for ETFs) gets an equal slot;
   the slot is held while the asset's 12-month return is positive, else it sits in cash.
   Decided on Fridays (the view at that Friday's DECIDE_AT); other days repeat it. A Friday
   counts once a bar that closed at or after its ETF close is stored (on a market-holiday
   Friday the research counted it from 22:30, the live book from Saturday's first close).
   The decision's date is the day of the latest close it can see (the harness's `View.today`).
2. sigma: the volatility of `tsmom12`'s own daily returns over the 52 complete Monday-Sunday
   weeks up to the month's previous day (weekly sums, sample std, x sqrt 52). None until all 52
   weeks lie after `tsmom12`'s first invested day.
3. For the decisions dated in a month, k solves mean(min(1, k / sigma_m)) = 70% over every
   monthly sigma known by its 1st (an expanding window: no later sigma is used), and the share
   of `tsmom12` is min(1, k / sigma) with that month's sigma. Capped at 100%: no leverage. The
   rest is cash.
4. Warm-up: until 24 monthly sigmas exist, or while this month's sigma is unknown, the share is
   the target, 70%. A sigma of 0 (`tsmom12` all in cash a whole year) keeps the previous share.

The expanding window starts with `PRIOR`: the research run's monthly sigmas 1995-03..2025-10
(`research/lib/ownvol_prior.py` regenerates them), all from bars that closed before 2025-11, so
none can see past a live decision. The live sigmas join it month by month once 52 weeks of the
book's own `tsmom12` exist in the stored bars. Without the prior, the stored history (from
2024-12) would keep the book at a fixed 70% until about 2029 (docs/DECISIONS.md 2026-11-24).

Differences from the research harness, all small: the live sigma uses close-to-close returns of
the stored bars with no costs and no T-bill rate (the research sleeve was costed, over T-bills,
on dividend-adjusted prices), and between resets the gym holds share x weights (1% band)
instead of letting the share drift until the next 1st.
"""

from __future__ import annotations

import bisect
import math
from datetime import UTC, date, datetime, timedelta
from functools import lru_cache

from grimstrade.data import ETF_CLOSE_UTC, UNIVERSE, History, close_time
from grimstrade.gym import DECIDE_AT, Strategy
from grimstrade.signals import BARS_PER_YEAR

TARGET = 0.70
WEEKS = 52
WARMUP = 24  # monthly sigmas before k is solved (risk-menu-3's card)
LOOKBACK_DAYS = 365
FRIDAY = 4

Weights = dict[str, float]


def month(d: date) -> str:
    return f"{d:%Y-%m}"


def first_of(d: date) -> date:
    return d.replace(day=1)


def next_month(d: date) -> date:
    return date(d.year + d.month // 12, d.month % 12 + 1, 1)


class Sleeve:
    """`tsmom12` rebuilt from the stored bars: Friday weights and daily returns. Every number
    here comes from bars in `history`, which hold only bars closed before the decision."""

    def __init__(self, history: History) -> None:
        self.syms = sorted(s for s, bars in history.items() if bars)
        self.dates = {s: [b.date for b in history[s]] for s in self.syms}
        self.closes = {s: [b.close for b in history[s]] for s in self.syms}
        self.shut = {s: [close_time(UNIVERSE[s], d) for d in self.dates[s]] for s in self.syms}
        # The decision's date, as the research harness dates it: the day of the latest close.
        clock = max((ts[-1] for ts in self.shut.values()), default=None)
        self.today = clock.date() if clock else None
        self.fridays: list[date] = []
        self.weights: list[Weights] = []
        self.ret: dict[date, float] = {}
        self.start: date | None = None  # first Friday with money in `tsmom12`
        if clock is None:
            return
        first = min(ds[0] for ds in self.dates.values())
        f = first + timedelta(days=(FRIDAY - first.weekday()) % 7)
        # A Friday counts once its ETF close is in: a late run early on Friday (the one due
        # Thursday 22:30) keeps the week before's weights, and Friday's are not computed from
        # half a Friday.
        while datetime.combine(f, ETF_CLOSE_UTC, tzinfo=UTC) <= clock:
            w = self.on_friday(f)
            self.fridays.append(f)
            self.weights.append(w)
            if self.start is None and sum(w.values()) > 0:
                self.start = f
            f += timedelta(days=7)
        for s in self.syms:
            ds, cs = self.dates[s], self.closes[s]
            for i in range(1, len(ds)):
                x = self.held(ds[i] - timedelta(days=1)).get(s, 0.0)
                if x and cs[i - 1] > 0:
                    self.ret[ds[i]] = self.ret.get(ds[i], 0.0) + x * (cs[i] / cs[i - 1] - 1)

    def on_friday(self, f: date) -> Weights:
        """`tsmom12` as decided on Friday `f`, from the bars closed by its DECIDE_AT."""
        at = datetime.combine(f, DECIDE_AT, tzinfo=UTC)
        eligible: list[str] = []
        up: list[str] = []
        for s in self.syms:
            n = bisect.bisect_right(self.shut[s], at)
            if n < BARS_PER_YEAR[UNIVERSE[s]]:
                continue
            eligible.append(s)
            ds, cs = self.dates[s], self.closes[s]
            j = bisect.bisect_right(ds, ds[n - 1] - timedelta(days=LOOKBACK_DAYS)) - 1
            if j >= 0 and cs[j] > 0 and cs[n - 1] / cs[j] - 1 > 0:
                up.append(s)
        return {s: 1 / len(eligible) for s in up}

    def held(self, d: date) -> Weights:
        """The weights of the last Friday on or before `d` (none before the first)."""
        i = bisect.bisect_right(self.fridays, d) - 1
        return self.weights[i] if i >= 0 else {}

    def sigma(self, end: date) -> float | None:
        """Std of the trailing 52 complete Monday-Sunday weeks of returns up to `end`, x sqrt 52;
        None if those weeks do not all lie after the sleeve's start."""
        last_sun = end - timedelta(days=(end.weekday() + 1) % 7)
        mon0 = last_sun - timedelta(days=WEEKS * 7 - 1)
        if self.start is None or mon0 < self.start:
            return None
        wk = [0.0] * WEEKS
        for i in range(WEEKS * 7):
            wk[i // 7] += self.ret.get(mon0 + timedelta(days=i), 0.0)
        mean = math.fsum(wk) / WEEKS
        return math.sqrt(math.fsum((x - mean) ** 2 for x in wk) / (WEEKS - 1) * WEEKS)


@lru_cache(maxsize=256)
def solve_k(sigmas: tuple[float, ...], target: float) -> float:
    """k with mean(min(1, k / sigma)) = target over the given positive sigmas (bisection, as in
    `research/lib/riskmenu3_run.py`)."""
    lo, hi = 0.0, 10.0
    for _ in range(60):
        k = (lo + hi) / 2
        if math.fsum(min(1.0, k / s) for s in sigmas) / len(sigmas) < target:
            lo = k
        else:
            hi = k
    return (lo + hi) / 2


def plan(
    sigmas: dict[str, float | None],
    upto: str,
    target: float = TARGET,
    prior: tuple[tuple[str, float], ...] = (),
) -> tuple[float, str]:
    """(share, how) for the month `upto` (YYYY-MM), from the monthly sigmas known by then:
    `prior` (month, sigma) pairs, then `sigmas` (month -> sigma, None if unknown) for the months
    after the prior. Months after `upto` are ignored, so a later sigma cannot change the answer."""
    last_prior = prior[-1][0] if prior else ""
    seen = [s for m, s in prior if m <= upto]
    steps: list[tuple[int, float | None]] = []  # per month: (sigmas known, its sigma)
    for m in sorted(m for m in sigmas if last_prior < m <= upto):
        sg = sigmas[m]
        if sg is not None and sg > 0:
            seen.append(sg)
        steps.append((len(seen), sg))
    kept = False
    for n, sg in reversed(steps):  # a sigma of 0 keeps the month before's share
        if n < WARMUP:
            return target, "warm-up" + (", share kept" if kept else "")
        if sg is None:
            return target, "no sigma yet" + (", share kept" if kept else "")
        if sg > 0:
            k = solve_k(tuple(seen[:n]), target)
            return min(1.0, k / sg), f"sigma {sg:.1%}, k {k:.4f}" + (", share kept" if kept else "")
        kept = True
    return target, "warm-up" if len(seen) < WARMUP else "no sigma yet"


def own_vol(target: float, prior: tuple[tuple[str, float], ...]) -> Strategy:
    def decide(history: History) -> tuple[Weights, str]:
        sleeve = Sleeve(history)
        name = f"own-vol {target:.0%}"
        if sleeve.today is None or not sleeve.fridays:
            return {}, f"{name}: no stored bars before a Friday yet, stay in cash"
        this = first_of(sleeve.today)
        sigmas: dict[str, float | None] = {}
        m = first_of(min(ds[0] for ds in sleeve.dates.values()))
        while m <= this:
            sigmas[month(m)] = sleeve.sigma(m - timedelta(days=1))
            m = next_month(m)
        share, how = plan(sigmas, month(this), target, prior)
        base = sleeve.held(sleeve.today)
        weights = {s: share * w for s, w in base.items() if share * w > 0}
        held = ", ".join(f"{s} {w:.0%}" for s, w in sorted(weights.items())) or "all cash"
        return weights, f"{name}: share {share:.0%} ({how}) of tsmom12; {held}"

    return decide


# The research run's monthly sigmas, 1995-03..2025-10 (research/lib/ownvol_prior.py; months
# with a sigma of 0, 2001-12..2002-03 and 2003-05..06, are not in the window).
# fmt: off
PRIOR = (
    ("1995-03", 0.103400), ("1995-04", 0.102092), ("1995-05", 0.098446), ("1995-06", 0.097383),
    ("1995-07", 0.092517), ("1995-08", 0.096954), ("1995-09", 0.094459), ("1995-10", 0.091543),
    ("1995-11", 0.081827), ("1995-12", 0.071679), ("1996-01", 0.070620), ("1996-02", 0.076166),
    ("1996-03", 0.084443), ("1996-04", 0.091696), ("1996-05", 0.097399), ("1996-06", 0.101574),
    ("1996-07", 0.099995), ("1996-08", 0.102264), ("1996-09", 0.109853), ("1996-10", 0.116858),
    ("1996-11", 0.119149), ("1996-12", 0.123906), ("1997-01", 0.128629), ("1997-02", 0.127537),
    ("1997-03", 0.124739), ("1997-04", 0.126149), ("1997-05", 0.133823), ("1997-06", 0.143096),
    ("1997-07", 0.144661), ("1997-08", 0.143985), ("1997-09", 0.149980), ("1997-10", 0.150907),
    ("1997-11", 0.153318), ("1997-12", 0.155415), ("1998-01", 0.158775), ("1998-02", 0.175649),
    ("1998-03", 0.176740), ("1998-04", 0.172627), ("1998-05", 0.165998), ("1998-06", 0.159295),
    ("1998-07", 0.160236), ("1998-08", 0.161580), ("1998-09", 0.166419), ("1998-10", 0.176422),
    ("1998-11", 0.192360), ("1998-12", 0.195143), ("1999-01", 0.191876), ("1999-02", 0.183622),
    ("1999-03", 0.184229), ("1999-04", 0.185164), ("1999-05", 0.190551), ("1999-06", 0.192004),
    ("1999-07", 0.195231), ("1999-08", 0.202952), ("1999-09", 0.192488), ("1999-10", 0.187064),
    ("1999-11", 0.194371), ("1999-12", 0.189505), ("2000-01", 0.188248), ("2000-02", 0.190394),
    ("2000-03", 0.198315), ("2000-04", 0.209873), ("2000-05", 0.295914), ("2000-06", 0.300435),
    ("2000-07", 0.324848), ("2000-08", 0.328559), ("2000-09", 0.331029), ("2000-10", 0.333563),
    ("2000-11", 0.326209), ("2000-12", 0.339552), ("2001-01", 0.337240), ("2001-02", 0.331958),
    ("2001-03", 0.326056), ("2001-04", 0.314565), ("2001-05", 0.230254), ("2001-06", 0.222909),
    ("2001-07", 0.176781), ("2001-08", 0.151859), ("2001-09", 0.141587), ("2001-10", 0.124753),
    ("2001-11", 0.100621), ("2002-04", 0.009319), ("2002-05", 0.013415), ("2002-06", 0.013415),
    ("2002-07", 0.013415), ("2002-08", 0.013415), ("2002-09", 0.013415), ("2002-10", 0.013415),
    ("2002-11", 0.013415), ("2002-12", 0.013415), ("2003-01", 0.013415), ("2003-02", 0.013415),
    ("2003-03", 0.013415), ("2003-04", 0.009973), ("2003-07", 0.019551), ("2003-08", 0.036099),
    ("2003-09", 0.048675), ("2003-10", 0.058256), ("2003-11", 0.062268), ("2003-12", 0.065492),
    ("2004-01", 0.066288), ("2004-02", 0.071572), ("2004-03", 0.073228), ("2004-04", 0.077545),
    ("2004-05", 0.081600), ("2004-06", 0.091449), ("2004-07", 0.089791), ("2004-08", 0.089719),
    ("2004-09", 0.091633), ("2004-10", 0.086490), ("2004-11", 0.085434), ("2004-12", 0.085979),
    ("2005-01", 0.085544), ("2005-02", 0.083160), ("2005-03", 0.085408), ("2005-04", 0.085050),
    ("2005-05", 0.084017), ("2005-06", 0.077968), ("2005-07", 0.077786), ("2005-08", 0.074322),
    ("2005-09", 0.066337), ("2005-10", 0.068497), ("2005-11", 0.069980), ("2005-12", 0.071957),
    ("2006-01", 0.072117), ("2006-02", 0.076564), ("2006-03", 0.075247), ("2006-04", 0.076347),
    ("2006-05", 0.075335), ("2006-06", 0.079664), ("2006-07", 0.085373), ("2006-08", 0.089555),
    ("2006-09", 0.089399), ("2006-10", 0.088841), ("2006-11", 0.086913), ("2006-12", 0.084963),
    ("2007-01", 0.085737), ("2007-02", 0.080131), ("2007-03", 0.080389), ("2007-04", 0.086162),
    ("2007-05", 0.085720), ("2007-06", 0.079485), ("2007-07", 0.077838), ("2007-08", 0.079146),
    ("2007-09", 0.082340), ("2007-10", 0.082036), ("2007-11", 0.083265), ("2007-12", 0.086888),
    ("2008-01", 0.088570), ("2008-02", 0.092392), ("2008-03", 0.093365), ("2008-04", 0.087345),
    ("2008-05", 0.087253), ("2008-06", 0.087502), ("2008-07", 0.086211), ("2008-08", 0.080199),
    ("2008-09", 0.079663), ("2008-10", 0.083520), ("2008-11", 0.083195), ("2008-12", 0.083328),
    ("2009-01", 0.084763), ("2009-02", 0.082485), ("2009-03", 0.081544), ("2009-04", 0.080043),
    ("2009-05", 0.078546), ("2009-06", 0.079701), ("2009-07", 0.078497), ("2009-08", 0.078533),
    ("2009-09", 0.077036), ("2009-10", 0.069738), ("2009-11", 0.066488), ("2009-12", 0.073148),
    ("2010-01", 0.069192), ("2010-02", 0.075767), ("2010-03", 0.076035), ("2010-04", 0.077705),
    ("2010-05", 0.079708), ("2010-06", 0.090181), ("2010-07", 0.091524), ("2010-08", 0.099471),
    ("2010-09", 0.101002), ("2010-10", 0.104575), ("2010-11", 0.101156), ("2010-12", 0.101475),
    ("2011-01", 0.101679), ("2011-02", 0.094249), ("2011-03", 0.092750), ("2011-04", 0.093528),
    ("2011-05", 0.092442), ("2011-06", 0.082874), ("2011-07", 0.081624), ("2011-08", 0.076025),
    ("2011-09", 0.078495), ("2011-10", 0.084632), ("2011-11", 0.094062), ("2011-12", 0.097268),
    ("2012-01", 0.103082), ("2012-02", 0.103845), ("2012-03", 0.103690), ("2012-04", 0.102224),
    ("2012-05", 0.100585), ("2012-06", 0.102637), ("2012-07", 0.102113), ("2012-08", 0.097822),
    ("2012-09", 0.093062), ("2012-10", 0.082539), ("2012-11", 0.073418), ("2012-12", 0.066425),
    ("2013-01", 0.055499), ("2013-02", 0.063128), ("2013-03", 0.080595), ("2013-04", 0.146089),
    ("2013-05", 0.199097), ("2013-06", 0.196371), ("2013-07", 0.205752), ("2013-08", 0.214243),
    ("2013-09", 0.215358), ("2013-10", 0.216185), ("2013-11", 0.218756), ("2013-12", 0.262619),
    ("2014-01", 0.269950), ("2014-02", 0.275133), ("2014-03", 0.281780), ("2014-04", 0.272529),
    ("2014-05", 0.244995), ("2014-06", 0.248669), ("2014-07", 0.242630), ("2014-08", 0.235966),
    ("2014-09", 0.237829), ("2014-10", 0.241346), ("2014-11", 0.236517), ("2014-12", 0.155693),
    ("2015-01", 0.141968), ("2015-02", 0.135089), ("2015-03", 0.132318), ("2015-04", 0.122246),
    ("2015-05", 0.105738), ("2015-06", 0.084800), ("2015-07", 0.081428), ("2015-08", 0.082312),
    ("2015-09", 0.080874), ("2015-10", 0.076048), ("2015-11", 0.069347), ("2015-12", 0.069428),
    ("2016-01", 0.071361), ("2016-02", 0.082836), ("2016-03", 0.085459), ("2016-04", 0.082248),
    ("2016-05", 0.082919), ("2016-06", 0.088424), ("2016-07", 0.106203), ("2016-08", 0.106380),
    ("2016-09", 0.104877), ("2016-10", 0.105995), ("2016-11", 0.106498), ("2016-12", 0.101359),
    ("2017-01", 0.102318), ("2017-02", 0.093916), ("2017-03", 0.096643), ("2017-04", 0.105484),
    ("2017-05", 0.111828), ("2017-06", 0.118061), ("2017-07", 0.161304), ("2017-08", 0.241666),
    ("2017-09", 0.256309), ("2017-10", 0.264127), ("2017-11", 0.269461), ("2017-12", 0.287343),
    ("2018-01", 0.322806), ("2018-02", 0.344214), ("2018-03", 0.386470), ("2018-04", 0.397822),
    ("2018-05", 0.415706), ("2018-06", 0.422683), ("2018-07", 0.411132), ("2018-08", 0.371157),
    ("2018-09", 0.368260), ("2018-10", 0.363045), ("2018-11", 0.360057), ("2018-12", 0.338994),
    ("2019-01", 0.296275), ("2019-02", 0.261491), ("2019-03", 0.207363), ("2019-04", 0.171681),
    ("2019-05", 0.136378), ("2019-06", 0.120597), ("2019-07", 0.121465), ("2019-08", 0.115304),
    ("2019-09", 0.094457), ("2019-10", 0.111727), ("2019-11", 0.112941), ("2019-12", 0.135274),
    ("2020-01", 0.136073), ("2020-02", 0.138594), ("2020-03", 0.154733), ("2020-04", 0.245581),
    ("2020-05", 0.252030), ("2020-06", 0.256145), ("2020-07", 0.250456), ("2020-08", 0.255406),
    ("2020-09", 0.259602), ("2020-10", 0.255487), ("2020-11", 0.256677), ("2020-12", 0.259898),
    ("2021-01", 0.264463), ("2021-02", 0.289573), ("2021-03", 0.299023), ("2021-04", 0.248675),
    ("2021-05", 0.252369), ("2021-06", 0.301067), ("2021-07", 0.306800), ("2021-08", 0.312670),
    ("2021-09", 0.313967), ("2021-10", 0.316006), ("2021-11", 0.315106), ("2021-12", 0.308462),
    ("2022-01", 0.310554), ("2022-02", 0.312557), ("2022-03", 0.282150), ("2022-04", 0.278433),
    ("2022-05", 0.275656), ("2022-06", 0.221337), ("2022-07", 0.214756), ("2022-08", 0.196329),
    ("2022-09", 0.187224), ("2022-10", 0.172446), ("2022-11", 0.157398), ("2022-12", 0.152744),
    ("2023-01", 0.143281), ("2023-02", 0.086634), ("2023-03", 0.066909), ("2023-04", 0.039081),
    ("2023-05", 0.015438), ("2023-06", 0.013121), ("2023-07", 0.038906), ("2023-08", 0.045685),
    ("2023-09", 0.056309), ("2023-10", 0.059959), ("2023-11", 0.074289), ("2023-12", 0.083349),
    ("2024-01", 0.091322), ("2024-02", 0.094695), ("2024-03", 0.105540), ("2024-04", 0.125630),
    ("2024-05", 0.131799), ("2024-06", 0.139365), ("2024-07", 0.139096), ("2024-08", 0.147333),
    ("2024-09", 0.161033), ("2024-10", 0.174753), ("2024-11", 0.179702), ("2024-12", 0.199850),
    ("2025-01", 0.207495), ("2025-02", 0.209669), ("2025-03", 0.208380), ("2025-04", 0.199312),
    ("2025-05", 0.204092), ("2025-06", 0.198772), ("2025-07", 0.198828), ("2025-08", 0.192025),
    ("2025-09", 0.181831), ("2025-10", 0.175245),
)
# fmt: on

decide = own_vol(TARGET, PRIOR)
