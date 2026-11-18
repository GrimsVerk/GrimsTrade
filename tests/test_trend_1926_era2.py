"""Research run trend-1926, card 2 (`TREND_ERA=1962`): the 1962-2001 path of
research/lib/trend_1926.py, offline, on tiny fixtures.

- The era switch sets the period, the symbol prefix, the result file, the windows and the bar.
- The loader keeps 1961-01-01 to 2001-12-31: nothing before is used, nothing after is parsed.
- Five-session weeks with Friday holidays: a hand replay of `tsmom12` gives the gym's equity on
  every day, for both fills. In a week whose Friday is a holiday the gym fills the new signal
  one session after the calendar-Friday convention of the gym-free paper series; that, and
  nothing else, is what the replay check measures (`replay_gap`).
- The card-2 outcome is read mechanically ("crashes only" when the lead goes without 1973-74).
"""

from __future__ import annotations

import importlib.util
import io
import math
import random
import sys
import zipfile
from collections.abc import Callable, Iterator
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any

import pytest

from grimstrade import data

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
FIRST = date(1961, 1, 3)
SLIP = 0.0002
MODS = ("harness", "common", "stats", "trend_tune", "trend_1926")


@pytest.fixture(scope="module")
def lib() -> Iterator[dict[str, ModuleType]]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    saved_mods = {k: sys.modules.pop(k, None) for k in MODS}
    sys.path.insert(0, str(LIB))
    mods: dict[str, ModuleType] = {}
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("TREND_ERA", "1962")  # read once, when trend_1926 is imported
        for name in ("harness", "common", "trend_1926"):
            spec = importlib.util.spec_from_file_location(name, LIB / f"{name}.py")
            assert spec and spec.loader
            mod = importlib.util.module_from_spec(spec)
            sys.modules[name] = mod
            spec.loader.exec_module(mod)
            mods[name] = mod
    mods["trend_tune"] = sys.modules["trend_tune"]
    yield mods
    data.UNIVERSE.clear()
    data.UNIVERSE.update(saved_universe)
    sys.path[:] = saved_path
    for k, v in saved_mods.items():
        if v is None:
            sys.modules.pop(k, None)
        else:
            sys.modules[k] = v


def test_era_switch(lib: dict[str, ModuleType]) -> None:
    t = lib["trend_1926"]
    assert t.ERA == "1962"
    loaded, first_decision = (t.FIRST, t.LAST), t.START
    assert loaded == (date(1961, 1, 1), date(2001, 12, 31))
    assert first_decision == date(1962, 1, 2)  # 1961 is warm-up only
    assert t.sym("Mkt") == "F62-Mkt" and t.sym(t.BOOK) == "F62-ind10"  # no clash with era 1
    assert t.RESULT == "trend-1926-era2"
    assert [w.key for w in t.WINDOWS] == ["whole", "1962-81", "1982-01", "x1", "x2", "x3", "to1993"]
    assert t.KEYS == ("1962-81", "1982-01", "x3", "x1")


# --- loader ---


def factors_csv(rows: list[tuple[str, float, float]]) -> str:
    body = "".join(f"{d},{m:8.2f},    0.00,    0.00,{rf:8.2f}\n" for d, m, rf in rows)
    return f"Made from CRSP.\n\n,Mkt-RF,SMB,HML,RF\n{body}\nCopyright\n"


def industry_csv(days: list[str]) -> str:
    names = ",NoDur,Durbl,Manuf,Enrgy,HiTec,Telcm,Shops,Hlth,Utils,Other\n"
    vw = "".join(f"{d}," + ",".join(f"{0.1 * (j + 1):6.2f}" for j in range(10)) + "\n"
                 for d in days)  # fmt: skip
    ew = "".join(f"{d}," + ",".join(["  7.00"] * 10) + "\n" for d in days)
    return (
        "Missing data are indicated by -99.99 or -999.\n\n"
        f"  Average Value Weighted Returns -- Daily\n{names}{vw}\n\n"
        f"  Average Equal Weighted Returns -- Daily\n{names}{ew}"
    )


def put_zip(path: Path, name: str, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr(name, text.encode("latin1"))
    path.write_bytes(buf.getvalue())


def test_loader_keeps_1961_to_2001(lib: dict[str, ModuleType], tmp_path: Path) -> None:
    t = lib["trend_1926"]
    days = ["19601230", "19610103", "19611229", "20011231", "20020102"]
    snap = tmp_path / "french" / "2026-11-12"
    rows = [(d, 1.0 + k, 0.02) for k, d in enumerate(days)]
    put_zip(snap / "F-F_Research_Data_Factors_daily_CSV.zip", "f.csv", factors_csv(rows))
    put_zip(snap / "10_Industry_Portfolios_daily_CSV.zip", "i.csv", industry_csv(days))
    raw = t.load(tmp_path)
    assert raw.snapshot == "2026-11-12"
    # 1960 is before the window, 2002 is never parsed
    assert raw.days == [date(1961, 1, 3), date(1961, 12, 29), date(2001, 12, 31)]
    assert raw.ret["Mkt"].tolist() == pytest.approx([0.0202, 0.0302, 0.0402])  # Mkt-RF + RF
    assert raw.ret["Utils"].tolist() == pytest.approx([0.009] * 3)
    assert raw.rf.tolist() == pytest.approx([0.0002] * 3)
    put_zip(snap / "10_Industry_Portfolios_daily_CSV.zip", "i.csv", industry_csv(days[:3]))
    with pytest.raises(ValueError):
        t.load(tmp_path)  # the two files must agree on the sessions


# --- windows ---


def test_window_masks(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    t = lib["trend_1926"]
    w = {x.key: x for x in t.WINDOWS}
    years = (1962, 1972, 1973, 1974, 1981, 1982, 1987, 1993, 1994, 2001)
    ords = np.array([date(y, 6, 30).toordinal() for y in years])

    def m(key: str) -> list[bool]:
        return [bool(x) for x in w[key].mask(ords)]

    assert all(m("whole"))
    assert m("1962-81") == [True] * 5 + [False] * 5
    assert m("1982-01") == [False] * 5 + [True] * 5
    assert m("x1") == [True, True, False, False, True, True, True, True, True, True]
    assert m("x2") == [True] * 6 + [False] + [True] * 3
    assert m("x3") == [True, True, False, False, True, True, False, True, True, True]
    assert m("to1993") == [True] * 8 + [False] * 2
    edge = np.array([date(1972, 12, 31).toordinal(), date(1973, 1, 1).toordinal(),
                     date(1974, 12, 31).toordinal(), date(1975, 1, 1).toordinal()])  # fmt: skip
    assert w["x1"].mask(edge).tolist() == [True, False, False, True]


# --- fidelity on five-session weeks with Friday holidays ---


def holidays(last: date) -> set[date]:
    """Every third Friday is a holiday (far more than real life, so the signal flips in some of
    those weeks), plus a few other weekday holidays."""
    out = {date(1961, 7, 4), date(1962, 1, 1), date(1962, 11, 22), date(1963, 12, 25)}
    fri = FIRST + timedelta(days=(4 - FIRST.weekday()) % 7)
    k = 0
    while fri <= last:
        if k % 3 == 2:
            out.add(fri)
        fri += timedelta(days=7)
        k += 1
    return out


def sessions(n_days: int) -> list[date]:
    off = holidays(FIRST + timedelta(days=n_days))
    every = [FIRST + timedelta(days=k) for k in range(n_days)]
    return [d for d in every if d.weekday() < 5 and d not in off]


def wave(n: int, seed: int = 3) -> list[float]:
    rng = random.Random(seed)
    return [round(rng.gauss(0.002 * math.sin(2 * math.pi * k / 260), 0.01), 4) for k in range(n)]


def gym_friday(days: list[date], decided: date) -> date:
    """The gym's week: the Friday on or before the latest session closed by the decision."""
    today = max(x for x in days if x <= decided)
    return today - timedelta(days=(today.weekday() - 4) % 7)


def calendar_friday(days: list[date], decided: date) -> date:
    """The paper series' week: the calendar Friday on or before the decision day."""
    return decided - timedelta(days=(decided.weekday() - 4) % 7)


Friday = Callable[[list[date], date], date]


def hand_replay(
    days: list[date], ret: list[float], start: date, late: bool, friday: Friday
) -> dict[date, float]:
    """`tsmom12` on one asset from the card's words, no gym: the decision in force at a bar's
    open is the one made the calendar day before, from the bars up to that week's Friday; a fill
    at the open costs 2 bps. Primary: open = previous close. Late: open = that day's close."""
    close = [100.0]
    for x in ret:
        close.append(close[-1] * (1 + x))
    close = close[1:]
    eq, pos = 1.0, False
    out: dict[date, float] = {}
    for i, d in enumerate(days):
        if d <= start:
            continue
        ratio = close[i] / close[i - 1]
        fri = friday(days, d - timedelta(days=1))
        seen = [k for k, x in enumerate(days) if x <= fri]
        last = seen[-1]
        base = max((k for k in seen if days[k] <= days[last] - timedelta(days=365)), default=None)
        want = len(seen) >= 252 and base is not None and close[last] > close[base]
        if late and pos:
            eq *= ratio
        if want != pos:
            eq = eq / (1 + SLIP) if want else eq * (1 - SLIP)
            pos = want
        if not late and pos:
            eq *= ratio
        out[d] = eq
    return out


@pytest.fixture(scope="module")
def fixture_run(lib: dict[str, ModuleType]) -> SimpleNamespace:
    np: Any = pytest.importorskip("numpy")
    t, h = lib["trend_1926"], lib["harness"]
    days = sessions(1400)
    ret = wave(len(days))
    raw = t.Raw("test", days, {"X": np.array(ret)}, np.zeros(len(days)))
    out = SimpleNamespace(days=days, ret=ret, raw=raw, runs={}, u={})
    for late in (False, True):
        u = t.universe(raw, ["X"], "X", late)
        assert u.start == t.START == date(1962, 1, 2)
        out.u[late] = u
        out.runs[late] = h.run("t", "rule", t.rule(), panel=u.panel, history=u.hist,
                               start=u.start, end=u.end, log=False)  # fmt: skip
    return out


@pytest.mark.parametrize("late", [False, True])
def test_gym_matches_hand_replay(
    lib: dict[str, ModuleType], fixture_run: SimpleNamespace, late: bool
) -> None:
    t = lib["trend_1926"]
    run, u, days = fixture_run.runs[late], fixture_run.u[late], fixture_run.days
    want = hand_replay(days, fixture_run.ret, t.START, late, gym_friday)
    got = dict(zip(run.days, run.equity / 10_000.0, strict=True))
    flips = sum(1 for a, b in zip(run.decisions, run.decisions[1:], strict=False)
                if bool(a.weights) != bool(b.weights))  # fmt: skip
    assert flips >= 6  # the rule really trades in this fixture
    for d in days:
        if t.START < d <= u.end:
            assert got[d] == pytest.approx(want[d], rel=1e-9), d


def test_holiday_friday_weeks_are_the_only_replay_gap(
    lib: dict[str, ModuleType], fixture_run: SimpleNamespace
) -> None:
    np: Any = pytest.importorskip("numpy")
    t = lib["trend_1926"]
    days, ret = fixture_run.days, fixture_run.ret
    gym_eq = hand_replay(days, ret, t.START, False, gym_friday)
    cal_eq = hand_replay(days, ret, t.START, False, calendar_friday)
    sess = set(days)
    apart = []
    for prev, d in zip(days, days[1:], strict=False):
        if prev in gym_eq and d in gym_eq:
            g = gym_eq[d] / gym_eq[prev] - 1
            q = cal_eq[d] / cal_eq[prev] - 1
            if abs(g - q) > 1e-12:
                apart.append((d, g - q))
    assert apart, "the fixture must flip the signal in some holiday-Friday week"
    for d, _ in apart:
        # the first or second session after a Friday that had no session
        fri = calendar_friday(days, d - timedelta(days=1))
        after = [x for x in days if x > fri][:2]
        assert fri not in sess and d in after, d
    # the replay check against trend-tune's paper series sees exactly these gaps
    pr = t.Pair("X", fixture_run.runs[False], fixture_run.runs[False])
    total, worst = t.replay_gap(pr, fixture_run.u[False], t.sym("X"))
    assert worst == pytest.approx(max(abs(x) for _, x in apart), abs=1e-5)
    log_gap = math.log(gym_eq[days[-1]] / cal_eq[days[-1]])
    assert total == pytest.approx(log_gap, abs=1e-4)
    assert np.isfinite(total)


# --- the outcome, applied mechanically ---


def outcome(
    lib: dict[str, ModuleType], mp: pytest.MonkeyPatch, diffs: dict[tuple[str, str], float]
) -> str:
    t = lib["trend_1926"]

    def window_diff(pr: SimpleNamespace, w: Any, block: float = 20) -> SimpleNamespace:
        return SimpleNamespace(diff=diffs.get((pr.name, w.key), 0.1))

    def mechanism(so: SimpleNamespace, w: Any) -> SimpleNamespace:
        return SimpleNamespace(ratio=1.3, p=0.05)

    mp.setattr(t, "window_diff", window_diff)
    mp.setattr(t, "mechanism", mechanism)
    pairs = {n: SimpleNamespace(name=n) for n in (t.MKT, t.BOOK)}
    solos = {n: SimpleNamespace(name=n) for n in (t.MKT, *t.INDUSTRIES)}
    text = "\n".join(t.section_outcome(pairs, solos, SimpleNamespace(name="late")))
    return text.split("**Outcome: ")[1].split(".**")[0]


def test_outcome_labels(lib: dict[str, ModuleType], monkeypatch: pytest.MonkeyPatch) -> None:
    t = lib["trend_1926"]
    m, b = t.MKT, t.BOOK
    assert outcome(lib, monkeypatch, {}) == "A property"
    # the published shape: ahead over the whole period and both halves, not without 1973-74
    assert outcome(lib, monkeypatch, {(m, "x1"): -0.03, (m, "x3"): -0.02}) == "Crashes only"
    assert outcome(lib, monkeypatch, {(m, "x3"): -0.02}) == "Crashes only"
    down = {(m, "whole"): -0.01, (b, "whole"): -0.01, ("late", "whole"): -0.01}
    assert outcome(lib, monkeypatch, down) == "No"
    assert outcome(lib, monkeypatch, {(b, "whole"): -0.01}) == "Too fragile to call"
    assert outcome(lib, monkeypatch, {("late", "whole"): -0.01}) == "Too fragile to call"
    some = outcome(lib, monkeypatch, {(m, "1982-01"): -0.01})
    assert some == "Something remains, but short of the card's conditions for a property"
