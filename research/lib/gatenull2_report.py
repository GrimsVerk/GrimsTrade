"""Lane gate-null-2: tables for Parts 1-2 (size and power) from the saved simulation cells,
and the Part 3 re-score table from research/results/gate-null-2-rescore/*.json. Applies the
card's decision rule (research/cards/gate-null-2.md) mechanically.

Run:  `uv run python -I research/lib/gatenull2_report.py`
Output: research/results/gate-null-2.md
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gatenull2 as g  # noqa: E402
import gatenull2_sim as sim  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
SIMS = 2000
NOM1, NOM2 = 1 / 41, 2 / 41
SHORT = ["F1", "F1b", "F2", "F3", "F4", "F5"]


def load(ret: str, dose: str, n: int) -> dict[str, np.ndarray]:
    z = np.load(sim.cache_dir() / f"{ret}_{dose}_T{n}_S{SIMS}.npz")
    return {k: z[k] for k in z.files}


def ranks(t: np.ndarray) -> np.ndarray:
    """(sims, families) rank of the true t (column 0) among each family's 40 (1 = highest)."""
    m = sim.M
    return np.column_stack(
        [g.rank_high(t[:, 0], t[:, 1 + m * f : 1 + m * (f + 1)]) for f in range(len(sim.FAMS))]
    )


def rates(t: np.ndarray) -> dict[str, Any]:
    rk = ranks(t)
    tc = t[:, 0] >= 2
    gate = (rk <= 2) & tc[:, None]
    return {
        "t2": float(tc.mean()),
        "r1": (rk == 1).mean(axis=0),
        "r2": (rk <= 2).mean(axis=0),
        "gate": gate.mean(axis=0),
        "both12": float((gate[:, 0] & gate[:, 2]).mean()),
        "both13": float((gate[:, 0] & gate[:, 3]).mean()),
    }


def diag(t: np.ndarray) -> list[tuple[float, float]]:
    """Per family: mean correlation (across simulations) of the true t with a placebo t, and
    mean pairwise correlation among the family's placebo t."""
    out = []
    m = sim.M
    for f in range(len(sim.FAMS)):
        blk = t[:, 1 + m * f : 1 + m * (f + 1)].astype(float)
        c = np.corrcoef(np.column_stack([t[:, 0], blk]).T)
        out.append((float(c[0, 1:].mean()), float(c[1:, 1:][np.triu_indices(m, 1)].mean())))
    return out


def pct(v: float) -> str:
    return f"{100 * v:.1f}"


def size_tables(lines: list[str], key: str, rets: list[str], ts: list[int], doses: list[str],
                fams: list[int]) -> dict[tuple[str, str, int], dict[str, Any]]:  # fmt: skip
    allr: dict[tuple[str, str, int], dict[str, Any]] = {}
    for ret in rets:
        lines += [
            f"**Returns `{ret}`** (cells: P(rank <= 2) / gate-rule false pass, %; nominal"
            " 4.9 / at most 4.9)",
            "",
            "| Dose | T | P(t >= 2) | " + " | ".join(sim.FAMS[f] for f in fams) + " | both F1+F2 |"
            " both F1+F3 |",
            "|---|---:|---:|" + "---:|" * (len(fams) + 2),
        ]
        for n in ts:
            for d in doses:
                r = rates(load(ret, d, n)[key])
                allr[(ret, d, n)] = r
                cells = [f"{pct(r['r2'][f])} / {pct(r['gate'][f])}" for f in fams]
                lines.append(
                    f"| {d} | {n} | {pct(r['t2'])} | " + " | ".join(cells)
                    + f" | {pct(r['both12'])} | {pct(r['both13'])} |"
                )  # fmt: skip
        lines.append("")
    return allr


def rank1_table(lines: list[str]) -> None:
    lines += [
        "P(rank = 1 of 41) under the null, % (nominal 2.4), NW 3, next month:",
        "",
        "| Returns | Dose | T | " + " | ".join(SHORT) + " |",
        "|---|---|---:|" + "---:|" * len(SHORT),
    ]
    for ret in sim.RETS:
        for n in sim.TS:
            for d in sim.DOSES:
                r = rates(load(ret, d, n)["t3"])
                lines.append(f"| {ret} | {d} | {n} | " + " | ".join(pct(v) for v in r["r1"]) + " |")
    lines.append("")


def diag_table(lines: list[str]) -> None:
    lines += [
        "Why: mean correlation of the true t with a placebo t / mean correlation among the 40"
        " placebo t of one family (across 2,000 null simulations; `garch-t`, T = 600, NW 3).",
        "",
        "| Dose | " + " | ".join(SHORT) + " |",
        "|---|" + "---:|" * len(SHORT),
    ]
    for d in sim.DOSES:
        dg = diag(load("garch-t", d, 600)["t3"])
        lines.append(f"| {d} | " + " | ".join(f"{a:+.2f} / {b:+.2f}" for a, b in dg) + " |")
    lines.append("")


def power(ret: str, d: str, n: int) -> dict[str, np.ndarray]:
    tp = load(ret, d, n)["tp"]
    out: dict[str, list[float]] = {
        k: [] for k in ("t2", "F1", "F1b", "F2", "F3", "F5", "b12", "b13")
    }
    for j in range(len(sim.R2S)):
        t = tp[j]
        rk = ranks(t)
        tc = t[:, 0] >= 2
        gate = (rk <= 2) & tc[:, None]
        out["t2"].append(float(tc.mean()))
        for f, name in ((0, "F1"), (1, "F1b"), (2, "F2"), (3, "F3"), (5, "F5")):
            out[name].append(float(gate[:, f].mean()))
        out["b12"].append(float((gate[:, 0] & gate[:, 2]).mean()))
        out["b13"].append(float((gate[:, 0] & gate[:, 3]).mean()))
    return {k: np.array(v) for k, v in out.items()}


def power_tables(lines: list[str]) -> dict[tuple[str, str, int], dict[str, np.ndarray]]:
    allp = {}
    cols = ["t2", "F1", "F1b", "F2", "F3", "F5", "b12", "b13"]
    head = ["t >= 2 alone", "F1", "F1b", "F2", "F3", "F5", "both F1+F2", "both F1+F3"]
    for ret in ("garch-t", "real"):
        for j, r2 in enumerate(sim.R2S):
            lines += [
                f"**Returns `{ret}`, planted R^2 {100 * r2:.2f}%** (gate-rule pass rate, %)",
                "",
                "| Dose | T | " + " | ".join(head) + " |",
                "|---|---:|" + "---:|" * len(head),
            ]
            for n in sim.TS:
                for d in sim.DOSES[:7]:
                    if d == "ar0.8":
                        continue
                    p = allp.setdefault((ret, d, n), power(ret, d, n))
                    lines.append(f"| {d} | {n} | " + " | ".join(pct(p[c][j]) for c in cols) + " |")
            lines.append("")
    return allp


def decide(lines: list[str], size: dict[tuple[str, str, int], dict[str, Any]],
           pw: dict[tuple[str, str, int], dict[str, np.ndarray]]) -> None:  # fmt: skip
    ar = [d for d in sim.DOSES if d.startswith("ar")]

    def missized(f: int, d: str) -> bool:
        return any(
            size[(r, d, n)]["r2"][f] > 1.5 * NOM2 or size[(r, d, n)]["gate"][f] > NOM2
            for r in ("garch-t", "real") for n in sim.TS
        )  # fmt: skip

    lines += ["## Decision rule applied (card, fixed before any number)", ""]
    for f, name in ((0, "F1 shift-earlier"), (1, "F1b shift-both")):
        bad = [d for d in ar if missized(f, d)]
        first = bad[0] if bad else None
        if first:
            phi = float(first[2:])
            ne = ", ".join(f"T = {n}: N_eff {n * (1 - phi) / (1 + phi):.0f}" for n in sim.TS)
            lines.append(f"- {name}: mis-sized at {', '.join(bad)}; threshold phi = {phi} ({ne}).")
        else:
            lines.append(f"- {name}: not mis-sized at any phi.")
    for f in (2, 3, 4, 5):
        ok = all(
            0.034 <= size[(r, d, n)]["r2"][f] <= 0.064 and size[(r, d, n)]["gate"][f] <= NOM2
            for r in ("garch-t", "real") for n in sim.TS for d in ar
        )  # fmt: skip
        worst = max(
            size[(r, d, n)]["r2"][f] for r in ("garch-t", "real") for n in sim.TS for d in ar
        )
        best = min(
            size[(r, d, n)]["r2"][f] for r in ("garch-t", "real") for n in sim.TS for d in ar
        )
        lines.append(
            f"- {sim.FAMS[f]}: P(rank <= 2) range {pct(best)}-{pct(worst)}% over AR doses, R1/R2,"
            f" both T: {'fixes it (inside 3.4-6.4%)' if ok else 'outside 3.4-6.4%'}."
        )
    lines.append("")
    j = sim.R2S.index(0.01)
    lines += [
        "Power at R^2 1%, T = 600 (gate-rule pass rate, %), and the null false-pass rate of the"
        " same rule (%), R1 / R2:",
        "",
        "| Dose | F1 power | F2 power | F3 power | both F1+F2 | both F1+F3 | F1 null | F2 null |"
        " F3 null | both F1+F2 null | both F1+F3 null |",
        "|---|" + "---:|" * 10,
    ]
    for d in ar:
        if d == "ar0.8":
            continue
        p = [pw[(r, d, 600)] for r in ("garch-t", "real")]
        s = [size[(r, d, 600)] for r in ("garch-t", "real")]

        def two(vals: list[float]) -> str:
            return " / ".join(pct(v) for v in vals)

        lines.append(
            f"| {d} | {two([x['F1'][j] for x in p])} | {two([x['F2'][j] for x in p])} |"
            f" {two([x['F3'][j] for x in p])} | {two([x['b12'][j] for x in p])} |"
            f" {two([x['b13'][j] for x in p])} | {two([x['gate'][0] for x in s])} |"
            f" {two([x['gate'][2] for x in s])} | {two([x['gate'][3] for x in s])} |"
            f" {two([x['both12'] for x in s])} | {two([x['both13'] for x in s])} |"
        )
    lines.append("")


RESCORE_COLS = ["gate", "true_t", "stored_rank", "shift_rank", "phase_rank", "iaaft_rank"]


def rescore_table(lines: list[str]) -> None:
    files = sorted((RES / "gate-null-2-rescore").glob("*.json"))

    def order(p: Path) -> tuple[int, str]:
        s = p.stem
        return (int(s[1:]) if s[0] in "WR" and s[1:].isdigit() else 99, s)

    lines += [
        "## Part 3: re-score of the gates on main (descriptive, no new verdict)",
        "",
        "Rank of the true t from the predicted side (1 = most extreme) among 40 placebos of each"
        " family; 'pass' = predicted sign, |t| >= 2 and rank <= 2. Null width: SD of the 40"
        " placebo t and their median. Dose acf1 / N_eff over the series that was surrogated.",
        "",
        "| Gate | True t (stored) | Shift rank (stored / rerun) | Shift SD, median"
        " | Phase rank | Phase SD, median | IAAFT rank | IAAFT SD, median | Dose acf1 | N_eff"
        " | Verdict change |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    skipped = []
    for p in sorted(files, key=order):
        r = json.loads(p.read_text())
        if r.get("reproduced") is False or "true_t" not in r:
            skipped.append(f"- {r['gate']}: {r.get('note', '')}")
            continue

        def nul(f: str, r: dict[str, Any] = r) -> str:
            if f"{f}_null" not in r:
                return "-"
            return f"{r[f'{f}_null']['sd']:.2f}, {r[f'{f}_null']['q50']:+.2f}"

        stored_pass = r.get("shift_pass", False)
        ph, ia = r.get("phase_pass", False), r.get("iaaft_pass", False)
        if stored_pass:
            ch = "pass stays under both" if ph and ia else "pass would fail 'both'"
        else:
            ch = "none (fails its own t or sign)" if r["sign"] * r["true_t"] < 2 else (
                "would pass under " + ", ".join(n for n, v in (("F2", ph), ("F3", ia)) if v)
                if ph or ia else "none")  # fmt: skip
        lines.append(
            f"| {r['gate']} | {r['true_t']:+.2f} ({r['stored_t']:+.2f}) |"
            f" {r['stored_rank']} / {r.get('shift_rank', '-')} | {nul('shift')} |"
            f" {r.get('phase_rank', '-')} | {nul('phase')} | {r.get('iaaft_rank', '-')} |"
            f" {nul('iaaft')} | {r['dose_acf1']:.3f} | {r['dose_neff']:.0f} | {ch} |"
        )
    lines.append("")
    if skipped:
        lines += ["Not re-scored:", "", *skipped, ""]
    notes = []
    for p in sorted(files, key=order):
        r = json.loads(p.read_text())
        notes.append(f"- {r['gate']}: {r.get('design', '')} {r.get('note', '')}".rstrip())
    lines += ["How each dose was surrogated:", "", *notes, ""]


def main() -> None:
    lines = [
        "# gate-null-2: size and power of placebo families (results)",
        "",
        "Card: `research/cards/gate-null-2.md` (pushed before any number). Script:",
        "`research/lib/gatenull2_sim.py` (cells), `research/lib/gatenull2_report.py` (this file),",
        "`research/lib/gatenull2_rescore_{a,b,c}.py` (Part 3). 2,000 simulations per cell, 40",
        "placebos per family, predicted sign +. Families: F1 x_{t-k}, k = 25..103 odd; F1b",
        "k = +-13..89 step 4; F2 phase-randomised; F3 IAAFT; F4 circular block bootstrap,",
        "24-month blocks; F5 random circular rotations. Gate rule: t >= 2 and rank <= 2 of 41.",
        "Binomial SE at 2,000: 0.34 points at 2.4%, 0.48 at 4.9%.",
        "",
        "## Part 1: size under the null",
        "",
        "### Main: next-month outcome, Newey-West 3 lags",
        "",
    ]
    fams = list(range(len(sim.FAMS)))
    size = size_tables(lines, "t3", sim.RETS, sim.TS, sim.DOSES, fams)
    rank1_table(lines)
    diag_table(lines)
    lines += ["### Shown: Newey-West 12 lags (next month)", ""]
    size_tables(lines, "t12", ["garch-t", "real"], sim.TS, sim.DOSES, [0, 1, 2, 3])
    lines += ["### Shown: 3-month overlapping outcome, Newey-West 3 lags (the W32 shape)", ""]
    size_tables(lines, "tq", ["garch-t", "real"], [300], sim.DOSES, [0, 1, 2, 3])
    lines += ["## Part 2: power (planted effect, NW 3, next month)", ""]
    pw = power_tables(lines)
    decide(lines, size, pw)
    rescore_table(lines)
    (RES / "gate-null-2.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
