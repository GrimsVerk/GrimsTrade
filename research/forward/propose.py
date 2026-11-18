"""Write research/forward/candidates.jsonl: the four rules lane forward-1 proposes to freeze.

PROPOSALS ONLY. Nothing here is frozen: the owner freezes (a later line in
research/forward/registry.jsonl, committed), after each rule has a forward adapter that emits
observations; the adapter's files join `code` and the hash changes then.

Code hashes are read from the research branches' commits named in `code_ref` (fetch them first):
    uv run python research/forward/propose.py
"""

from __future__ import annotations

import json
from pathlib import Path

from grimstrade import forward

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / forward.CANDIDATES
STATUS = "proposed by lane forward-1 on 2026-11-18; NOT frozen by the owner"
ALPHA = 0.025  # 0.10 one-sided over the four together (Bonferroni), per rule


def lib(*names: str) -> list[str]:
    return [f"research/lib/{n}.py" for n in names]


CANDIDATES = [
    dict(
        rule_id="carry-3-band@1",
        code_ref="a76a2e4f8c698e6f67fe95fcfcbf497752024da3",  # branch carry-3, PR #31
        paths=lib(
            "carry3",
            "carry3_engine",
            "carry3_cost",
            "carry3_panel",
            "breadth_books",
            "breadth_xs",
            "breadth_agg",
            "short1",
            "short_engine",
            "stats",
            "harness",
        ),
        params={
            "rebalance": "weekly",
            "signal": "7-day average funding rate",
            "long": "third of perps with the lowest funding",
            "short": "third of perps with the highest funding",
            "band": "a held coin stays until it leaves its half of the ranking; small weight "
            "changes are not traded",
            "book_usd": 10000,
            "costs": "carry-3 model: ~8 bps a side (5 fee, 1.5 half-spread, 1.5 impact) plus "
            "every funding payment",
        },
        data={
            "source": "public keyless perp endpoints: Binance USDT-M outside the 30, Bybit "
            "linear, Hyperliquid (funding history and daily klines)",
            "universe": "every perp listed at each weekly decision, delisted ones kept",
            "mode": "live: list snapshots must be recorded weekly (later downloads drop "
            "delisted coins)",
        },
        plan=forward.Plan("sharpe", effect=0.79, per_year=52, alpha=ALPHA),
        source="carry-3 (PR #31): train 2021-02..2025-11 pooled Sharpe 0.79 (p 0.025); held-out "
        "2025-11..2026-11 -0.65 (failed, year spent); rl-6 (PR #52): ~7 years at p < 0.10",
        note="Value = the book's weekly return after costs and funding. Effect is the train "
        "Sharpe, the optimistic number; the held-out year was -0.65. Adapter needed: carry3.py "
        "stops at TRAIN_END/HELD_END.",
    ),
    dict(
        rule_id="fomc-bond-drift@1",
        code_ref="9e4f93b72e1e9305dc8ac4bf85c62fc9ca63b80a",  # branch ann-1, PR #65
        paths=lib("ann1_event", "survey2_fomc", "macro"),
        params={
            "event": "scheduled FOMC statement day (day 0)",
            "value": "TLT dividend-adjusted return close(day -1) to close(day 0), minus the "
            "mean TLT daily return over the 250 trading days before day -1 that are not "
            "FOMC days; bps",
        },
        data={
            "source": "TLT daily bars (Yahoo chart; raw close plus dividends on ex-dates)",
            "calendar": "federalreserve.gov FOMC meeting calendar, scheduled meetings only",
            "mode": "replayable",
        },
        plan=forward.Plan("mean", effect=12.0, per_year=8, alpha=ALPHA, sd=107.0),
        source="survey-2 S3 (Pan and Peng 2025; Hillenbrand, RFS 2025): ~12 bps a meeting; "
        "ann-1 (PR #65): TLT day 0 +26.5 bps over other days 2015-2025 (t 2.3, 87 meetings, "
        "in the papers' own sample, 1 of ~70 cells)",
        note="sd 107 bps = 26.5 / 2.3 * sqrt(87), from ann-1's cell. Effect is the papers' 12 "
        "bps; at ann-1's 26.5 it would need ~16 years. Descriptive close-to-close; the gym "
        "could only trade open-to-open. Adapter needed: ann1_event.py stops at 2025-11-09.",
    ),
    dict(
        rule_id="coin-stop-0.25@1",
        code_ref="5c9dba582a2c9b77fa1693460c4a121eecc53523",  # branch coin-cap-2, PR #53
        paths=lib(
            "coin_cap2",
            "coin_cap2_core",
            "cointop1",
            "cointop1_core",
            "breadth_books",
            "breadth_xs",
            "stats",
            "harness",
        ),
        params={
            "rule": "stop-0.25 on the coin slots of tsmom12, checked weekly",
            "episode": "a coin of breadth-1's top-100 book falls 60% or more; falls grouped "
            "into episodes as in coin-cap-2",
            "compare": "a cap on the coin slot of matched cost (0.663 of the slot)",
            "value": "cap's deepest loss minus the stop's deepest loss in the episode "
            "(> 0: the stop wins)",
        },
        data={
            "source": "Coin Metrics community data, breadth-1's top-100 coin book, dead coins kept",
            "mode": "replayable",
        },
        plan=forward.Plan("win_rate", effect=15 / 21, per_year=1.6, alpha=ALPHA),
        source="coin-cap-2 (PR #53): stop ahead of the matched cap in 15 of 21 episodes "
        "2013-2025 (sign p 0.039); coin-cap-3 (PR #56): not significant against all 13 "
        "coin-cap picks",
        note="21 episodes in ~13 years = 1.6 a year, but only 7.6 effectively independent in "
        "10 years: by that count the years needed double. A risk choice (shallower worst loss, "
        "same Sharpe), so the forward test cannot settle the owner's decision in time.",
    ),
    dict(
        rule_id="eu-monthly-vs-weekly@1",
        code_ref="b2a3ef4d7aac3cc8a71b5197a4a643712a34bfea",  # branch eu-3, PR #63
        paths=[*lib("eu3", "eu2", "eu1", "common", "harness"), "src/grimstrade/gym.py"],
        params={
            "book": "euw: SXR8, EXSA, IQQE, IBGS, IBGL, 4GLD, EXXY",
            "signal": "365-day return > 0 (tsmom12), unchanged",
            "a": "V1: signal checked and trades placed only on the last Friday of each month",
            "b": "R: house rule (Friday signal, weights repeated daily, 1% band)",
            "value": "weekly return of a minus weekly return of b, EUR, no fixed fee",
        },
        data={
            "source": "Yahoo chart UCITS lines in EUR (eu-1's set)",
            "mode": "replayable",
        },
        plan=forward.Plan("sharpe", effect=0.50, per_year=52, alpha=ALPHA),
        source="eu-3 (PR #63): monthly +0.14 Sharpe over weekly at no fee, one-sided bootstrap "
        "p 0.03 over 2012-2025 (best of 6 variants; on the US six 1994-2025 monthly was worse)",
        note="Effect 0.50 = the annual signal-to-noise of the difference implied by p 0.03 over "
        "~14 years (z 1.88 / sqrt(14)). Probably inflated (best of six). The fee saving of a "
        "monthly clock is mechanical and needs no forward test; only the edge does.",
    ),
]


def main() -> None:
    lines = []
    for c in CANDIDATES:
        paths = c["paths"]
        assert isinstance(paths, list)
        ref = str(c["code_ref"])
        row = forward.entry(
            str(c["rule_id"]),
            code=forward.code_hashes(REPO, paths, ref=ref),
            code_ref=ref,
            params=c["params"],  # type: ignore[arg-type]
            data=c["data"],  # type: ignore[arg-type]
            plan=c["plan"],  # type: ignore[arg-type]
            source=str(c["source"]),
            note=str(c["note"]),
        )
        lines.append(json.dumps({"status": STATUS, **row}, sort_keys=True))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
