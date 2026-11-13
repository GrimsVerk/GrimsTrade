"""Zero-shot Chronos forecasts for run fm-1 (card: research/fm-1.md). GPU, throwaway env:

    uv run --with torch --with chronos-forecasting \
        python -I research/lib/fm1_forecast.py <model> [--check]

<model> is one of MODELS. Weights: official Amazon repos, safetensors only (only `*.json` and
`*.safetensors` are downloaded, at a pinned commit), no remote code. Writes
research/data/fm/<model>.npz (forecasts) and <model>.json (revision, GPU time, peak memory).
Every context ends at the decision bar's close; nothing later is passed to the model.
"""

from __future__ import annotations

import json
import resource
import sys
import time
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_hf  # noqa: E402
import rl2_data  # noqa: E402

MODELS = {
    "bolt-small": "amazon/chronos-bolt-small",
    "bolt-base": "amazon/chronos-bolt-base",
    "chronos2": "amazon/chronos-2",
}
CTX = 512
BATCH = 256
WEEK_FROM = date(1996, 1, 5)  # two years of forecasts before 2000 for the gate's sd_past
DAY_FROM = date(2000, 1, 1)
HOUR_FROM = int(datetime(2023, 1, 1, tzinfo=UTC).timestamp())
COINS = ["btc-binance", "eth-binance"]
OUT = Path(__file__).resolve().parents[1] / "data" / "fm"


def load(name: str):  # type: ignore[no-untyped-def]
    import torch
    from chronos import BaseChronosPipeline
    from huggingface_hub import HfApi, snapshot_download

    repo = MODELS[name]
    sha = HfApi().model_info(repo).sha
    path = snapshot_download(repo, revision=sha, allow_patterns=["*.json", "*.safetensors"])
    assert list(Path(path).glob("*.safetensors")), "no safetensors weights"
    pipe = BaseChronosPipeline.from_pretrained(
        path, device_map="cuda", torch_dtype=torch.bfloat16, use_safetensors=True
    )
    return pipe, sha


def median(pipe, ctxs: list[np.ndarray], steps: list[int]) -> np.ndarray:  # type: ignore[no-untyped-def]
    """[len(ctxs), len(steps)] median forecast at the given 1-based horizons."""
    import torch

    out = np.full((len(ctxs), len(steps)), np.nan)
    h = max(steps)
    idx = [s - 1 for s in steps]
    for b in range(0, len(ctxs), BATCH):
        xs = [torch.tensor(c, dtype=torch.float32) for c in ctxs[b : b + BATCH]]
        q, _ = pipe.predict_quantiles(xs, prediction_length=h, quantile_levels=[0.5])
        if isinstance(q, list):  # Chronos-2: one [variates, h, Q] tensor per series
            q = torch.stack([x[0] for x in q])
        out[b : b + len(xs)] = q[:, idx, 0].float().cpu().numpy()
    return out


def weekly(pipe, book: str = "six", invert: bool = False) -> dict[str, np.ndarray]:  # type: ignore[no-untyped-def]
    """Friday forecasts for a book; `invert` feeds 1 / price (the memorisation check)."""
    t = rl2_data.load()[book].t
    cl = 1 / t.book.closes if invert else t.book.closes
    n = cl.shape[1]
    fc = np.full((len(t.fridays), n), np.nan)
    jobs, ctxs, steps = [], [], []
    for i, (d, k) in enumerate(zip(t.fridays, t.kf, strict=True)):
        if d < (date(1964, 1, 3) if book == "gspc" else WEEK_FROM):
            continue
        for j in range(n):
            c = cl[: k + 1, j]
            c = c[np.isfinite(c)]
            if len(c) < 64 or not np.isfinite(cl[k, j]):
                continue
            jobs.append((i, j))
            ctxs.append(c[-CTX:])
            steps.append(7 if t.book.crypto[j] else 5)
    for hz in (5, 7):
        sel = [m for m, s in enumerate(steps) if s == hz]
        med = median(pipe, [ctxs[m] for m in sel], [hz])[:, 0]
        for m, v in zip(sel, med, strict=True):
            i, j = jobs[m]
            fc[i, j] = np.log(v / ctxs[m][-1]) if v > 0 else np.nan
    return {"week_fc": fc}


def daily(pipe) -> dict[str, np.ndarray]:  # type: ignore[no-untyped-def]
    t = rl2_data.load()["six"].t
    cl = t.book.closes
    k0 = t.book.day(DAY_FROM)
    fc = np.full(cl.shape, np.nan)
    for j in range(cl.shape[1]):
        ks = np.flatnonzero(np.isfinite(cl[:, j]))
        pos = {int(k): p for p, k in enumerate(ks)}
        series = cl[ks, j]
        todo = [int(k) for k in ks if k >= k0 and pos[int(k)] >= 63]
        ctxs = [series[max(0, pos[k] - CTX + 1) : pos[k] + 1] for k in todo]
        med = median(pipe, ctxs, [1])[:, 0]
        for k, c, v in zip(todo, ctxs, med, strict=True):
            fc[k, j] = np.log(v / c[-1]) if v > 0 else np.nan
    return {"day_fc": fc}


def hourly(pipe) -> dict[str, np.ndarray]:  # type: ignore[no-untyped-def]
    out = {}
    for name in COINS:
        h = breadth_hf.load(name)
        price = np.exp(h.lc)
        todo = np.flatnonzero((h.t >= HOUR_FROM) & (np.arange(len(h.t)) >= CTX))
        ctxs = [price[i - CTX + 1 : i + 1] for i in todo]
        med = median(pipe, ctxs, [1, 24])
        fc = np.full((len(h.t), 2), np.nan)
        fc[todo] = np.log(med / price[todo][:, None])
        out[f"{name}_fc"] = fc
        out[f"{name}_t"] = h.t
    return out


def check(name: str) -> None:
    """Leak checks (research/fm-1.md, "Memorisation checks"): weekly forecasts of the six assets
    fed 1 / price, and of the out-of-universe books."""
    pipe, _ = load(name)
    res = {"six_inv": weekly(pipe, "six", invert=True)["week_fc"]}
    for book in ("etf", "coin", "idx", "sec", "gspc"):
        res[book] = weekly(pipe, book)["week_fc"]
    np.savez_compressed(OUT / f"{name}-check.npz", **res)
    print(name, "check done", flush=True)


def main(name: str) -> None:
    import torch

    OUT.mkdir(parents=True, exist_ok=True)
    pipe, sha = load(name)
    torch.cuda.reset_peak_memory_stats()
    res: dict[str, np.ndarray] = {}
    timing = {}
    for job in (weekly, daily, hourly):
        t0 = time.time()
        res.update(job(pipe))
        torch.cuda.synchronize()
        timing[job.__name__] = round(time.time() - t0, 1)
        print(name, job.__name__, timing[job.__name__], "s", flush=True)
    np.savez_compressed(OUT / f"{name}.npz", **res)
    meta = {
        "model": MODELS[name], "revision": sha, "dtype": "bfloat16", "context": CTX,
        "seconds": timing, "gpu": torch.cuda.get_device_name(0),
        "peak_gpu_mb": round(torch.cuda.max_memory_allocated() / 2**20),
        "peak_rss_mb": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024),
        "run_at": datetime.now(UTC).strftime("%Y-%m-%d %H:%M"),
    }  # fmt: skip
    (OUT / f"{name}.json").write_text(json.dumps(meta, indent=1))
    print(meta, flush=True)


if __name__ == "__main__":
    if "--check" in sys.argv:
        check(sys.argv[1])
    else:
        main(sys.argv[1])
