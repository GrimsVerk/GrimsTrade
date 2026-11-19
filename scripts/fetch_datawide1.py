"""Download the keyless sources verified by research run data-wide-1 into the raw-data cache.

    uv run python -I scripts/fetch_datawide1.py            # every source
    uv run python -I scripts/fetch_datawide1.py usgs gpr   # some sources

Cache root: `cache_root` in the git-ignored `research/macro.local.json` (copy the committed
`.example`). Files land in `<root>/data-wide-1/<source>/<YYYY-MM-DD>/` (one dated snapshot per
run, so later runs sit beside earlier ones and nothing is overwritten). Each file is written
once (temp file + rename); a rerun on the same day skips files already there. One line per new
file is appended to `<root>/manifest.jsonl` (path, fetched_at, url, bytes, sha256), as
`scripts/fetch_info1.py` does. Never commit the downloaded files; read them as data only
(`python -I`), never execute them. A source that answers with an HTML page (bot check, login)
instead of data is skipped and reported, never worked around. Polite: one request at a time,
a pause between requests, a generic User-Agent.

Sources (all keyless; terms in research/data-wide-1.md):
- usgs:      USGS ComCat earthquakes, M >= 6 since 1900 and M >= 5 since 1973 (CSV).
- gpr:       Caldara-Iacoviello geopolitical risk, daily (1985-) and monthly (1900-) (XLS).
- gprvint:   six archived daily GPR vintages from the authors' GitHub (to read the lag).
- nuc:       EIA bulk file NUC_STATUS (daily US nuclear outages by plant, 2007-) (ZIP).
- flu:       Delphi Epidata FluView, US national ILI, latest issue plus one early vintage (JSON).
- hacks:     DefiLlama hacks list (JSON).
- fdic:      FDIC BankFind bank failures since 1934 (JSON).
- portwatch: IMF PortWatch daily chokepoint transits (2019-) (JSON pages).
- mof:       Japan Ministry of Finance FX intervention operations (1991-) (CSV).
- kev:       CISA Known Exploited Vulnerabilities catalogue (2021-) (CSV).
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

UA = "grimstrade-research/0.1 (non-commercial research; python urllib)"
PAUSE_S = 1.5
TODAY = datetime.now(UTC).date().isoformat()
USGS = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&orderby=time-asc"
PORTWATCH = (
    "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/"
    "Daily_Chokepoints_Data/FeatureServer/0/query?where=1%3D1&outFields=*"
    "&orderByFields=ObjectId&f=json"
)
PAGE = 2000
# Mondays, a Tuesday (2026-07-07) and month starts, spread over the archive (2022-02 onward).
GPR_VINTAGES = ["20220224", "20240701", "20260706", "20260707", "20261102", "20261109"]


def cache_root() -> Path:
    cfg = Path(__file__).resolve().parents[1] / "research" / "macro.local.json"
    return Path(json.loads(cfg.read_text())["cache_root"]).expanduser()


def jobs(source: str) -> list[tuple[str, str]]:
    """(file name, url) for one source. PortWatch pages are added while fetching."""
    if source == "usgs":
        out = [("m6_1900.csv", f"{USGS}&starttime=1900-01-01&minmagnitude=6")]
        edges = [1973, 1983, 1993, 2003, 2013, 2019, 2027]
        for a, b in zip(edges, edges[1:], strict=False):
            out.append(
                (f"m5_{a}_{b - 1}.csv", f"{USGS}&starttime={a}-01-01&endtime={b}-01-01"
                 "&minmagnitude=5")
            )  # fmt: skip
        return out
    if source == "gpr":
        base = "https://www.matteoiacoviello.com/gpr_files/"
        return [(n, base + n) for n in ("data_gpr_daily_recent.xls", "data_gpr_export.xls")]
    if source == "gprvint":  # a few archived daily vintages, to read the release lag
        base = (
            "https://raw.githubusercontent.com/iacoviel/iacoviel.github.io/master/"
            "gpr_archive_files/data_gpr_daily_recent_"
        )
        return [(f"{d}.xls", f"{base}{d}.xls") for d in GPR_VINTAGES]
    if source == "nuc":
        return [("NUC_STATUS.zip", "https://www.eia.gov/opendata/bulk/NUC_STATUS.zip")]
    if source == "flu":
        api = "https://api.delphi.cmu.edu/epidata/fluview/?regions=nat"
        return [
            ("fluview_nat_latest.json", f"{api}&epiweeks=199740-202652"),
            ("fluview_nat_issue201001.json", f"{api}&epiweeks=200940-201001&issues=201001"),
        ]
    if source == "hacks":
        return [("hacks.json", "https://api.llama.fi/hacks")]
    if source == "fdic":
        return [
            (
                "failures.json",
                "https://banks.data.fdic.gov/api/failures?limit=10000&sort_by=FAILDATE"
                "&sort_order=ASC&fields=CERT,NAME,FAILDATE,FAILYR,QBFASSET,QBFDEP,COST,"
                "RESTYPE,RESTYPE1,SAVR,PSTALP",
            )
        ]
    if source == "mof":
        return [
            (
                "foreign_exchange_intervention_operations.csv",
                "https://www.mof.go.jp/english/policy/international_policy/reference/feio/"
                "foreign_exchange_intervention_operations.csv",
            )
        ]
    if source == "kev":
        return [
            (
                "known_exploited_vulnerabilities.csv",
                "https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv",
            )
        ]
    raise ValueError(f"unknown source {source}")


SOURCES = ["usgs", "gpr", "gprvint", "nuc", "flu", "hacks", "fdic", "portwatch", "mof", "kev"]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return bytes(r.read())


def looks_like_html(body: bytes) -> bool:
    head = body[:512].lstrip().lower()
    return head.startswith(b"<!doctype html") or head.startswith(b"<html")


def save(root: Path, rel: str, url: str, body: bytes) -> None:
    dst = root / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + ".part")
    tmp.write_bytes(body)
    os.replace(tmp, dst)
    line = {
        "bytes": len(body),
        "fetched_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "path": rel,
        "sha256": hashlib.sha256(body).hexdigest(),
        "url": url,
    }
    data = (json.dumps(line, sort_keys=True) + "\n").encode()
    fd = os.open(root / "manifest.jsonl", os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, data)  # one write per line: O_APPEND keeps lines whole
    finally:
        os.close(fd)


def get_one(root: Path, rel: str, url: str) -> bytes | None:
    if (root / rel).exists():
        print(f"skip {rel}")
        return (root / rel).read_bytes()
    try:
        body = fetch(url)
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"FAIL {url}: {e}")
        return None
    finally:
        time.sleep(PAUSE_S)
    if looks_like_html(body):
        print(f"SKIP {url}: got an HTML page (login or bot check?), not saved")
        return None
    save(root, rel, url, body)
    print(f"ok   {rel} ({len(body)} bytes)")
    return body


def portwatch(root: Path, folder: str) -> int:
    """Page through the chokepoint layer until a page comes back short."""
    errors, offset = 0, 0
    while True:
        url = f"{PORTWATCH}&resultOffset={offset}&resultRecordCount={PAGE}"
        body = get_one(root, f"{folder}/page_{offset:07d}.json", url)
        if body is None:
            return errors + 1
        n = len(json.loads(body).get("features", []))
        if n < PAGE:
            return errors
        offset += PAGE


def main(argv: list[str]) -> int:
    root = cache_root()
    errors = 0
    for source in argv or SOURCES:
        folder = f"data-wide-1/{source}/{TODAY}"
        if source == "portwatch":
            errors += portwatch(root, folder)
            continue
        for name, url in jobs(source):
            if get_one(root, f"{folder}/{name}", url) is None:
                errors += 1
    print(f"DONE errors={errors}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
