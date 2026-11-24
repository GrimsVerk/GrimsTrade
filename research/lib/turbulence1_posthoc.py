"""turbulence-1, post hoc (after the logged run): overlap of the trigger days and what the
set did after them. Descriptive only, train data only, no backtest, no `tries.md` rows.

    uv run --with numpy python research/lib/turbulence1_posthoc.py

Appends its tables to `research/results/turbulence-1.md` under "Post hoc, after the run".
The matched percentiles are the ones the logged run found (results table).
"""

from __future__ import annotations

import common as c
import harness
import numpy as np
import turbulence1 as t

MATCHED = {"six": 90.141, "idx": 90.063}  # `mag-match` percentiles of the logged run
HEADING = "## Post hoc, after the run"
FWD = 20


def forward(grid: np.ndarray) -> np.ndarray:
    """Mean over the set's assets of the log return over the next FWD grid rows."""
    lr = np.diff(np.log(grid), axis=0)
    out = np.full(len(grid), np.nan)
    for i in range(len(grid) - FWD - 1):
        x = lr[i + 1 : i + FWD + 1]
        live = ~np.isnan(x).all(axis=0)
        out[i] = float(np.nanmean(np.nansum(x, axis=0)[live]))
    return out


def lines(name: str) -> list[str]:
    u = c.ctx(name)
    rows = t.window_rows(u.panel, u.start, u.end)
    sig = t.signals(u.panel.grid)
    on_t = t.trigger(sig["T"], 90)[rows]
    on_m = t.trigger(sig["M"], MATCHED[name])[rows]
    on_c = t.trigger(sig["C"], 90)[rows]
    both, either = int((on_t & on_m).sum()), int((on_t | on_m).sum())
    f = forward(u.panel.grid)[rows]
    out = [
        f"### `{name}`, {u.start}..{u.end}",
        "",
        f"Trigger days: `turb` {int(on_t.sum()):,}, `mag-match` {int(on_m.sum()):,}, both "
        f"{both:,} (Jaccard {both / either:.2f}); `turb` only {int((on_t & ~on_m).sum()):,}, "
        f"`mag-match` only {int((on_m & ~on_t).sum()):,}; `corr` {int(on_c.sum()):,} "
        f"(with `turb` {int((on_c & on_t).sum()):,}).",
        "",
        f"| Days | n | Next {FWD} grid days, mean log return of the set's assets |",
        "|---|---:|---:|",
    ]
    for label, mask in [
        ("all", np.ones(len(rows), dtype=bool)),
        ("`turb` on", on_t),
        ("`mag-match` on", on_m),
        ("`turb` only", on_t & ~on_m),
        ("`mag-match` only", on_m & ~on_t),
        ("`corr` on", on_c),
    ]:
        out.append(f"| {label} | {int(mask.sum()):,} | {100 * np.nanmean(f[mask]):+.2f}% |")
    return [*out, ""]


def main() -> None:
    assert harness.TRAIN_LAST_BAR.isoformat() == "2025-11-10"  # train only
    out = [
        HEADING,
        "",
        "Computed after the logged run (`lib/turbulence1_posthoc.py`), descriptive only: no "
        "backtest, no `tries.md` rows. Forward returns are overlapping windows, so the rows are "
        "far from independent.",
        "",
    ]
    for name in ("six", "idx"):
        out += lines(name)
    path = harness.RESEARCH / "results" / "turbulence-1.md"
    text = path.read_text()
    if HEADING in text:
        text = text[: text.index(HEADING)].rstrip() + "\n"
    path.write_text(text.rstrip() + "\n\n" + "\n".join(out).rstrip() + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
