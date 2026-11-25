"""stale-checks-1: rebuild the Schwert (1990) appendix transcription used by part (a).

    uv run python -I research/lib/stalechecks1_ocr.py PDF OUT_CSV [WORKDIR]

PDF is Schwert's NBER WP 2985 scan (www.nber.org/system/files/working_papers/w2985/w2985.pdf,
cached by survey-9 at `<cache_root>/survey-9/schwert/w2985.pdf`, sha256 a509de9d...f94842).
OUT_CSV is `<cache_root>/stale-checks-1/schwert-appendix-1884-1926.csv` (not committed;
sha256 4ea58998...94cf3a78 for the run in the write-up). Needs pdftoppm, ImageMagick (`magick`)
and tesseract on PATH.

Steps (the lane's run, unchanged):
1. Render PDF pages 50 and 51 (appendix "Monthly Index of Common Stock Returns, 1802-1987",
   rows 1851-1899 and 1900-1948) at 300, 400 and 500 dpi, grey; rotate 90 degrees (the table is
   landscape). The 500 dpi image is also thresholded at 60%.
2. Whole-page OCR (tesseract --psm 6) of each rendering; the 500 dpi one with a digit whitelist.
   Cell OCR: each of the 12 cells of rows 1884-1926 cropped from the 400 dpi page (column x from
   the table, row y from tesseract's word boxes for the year label, page skew corrected),
   upscaled 200%, thresholded at 50% and 65%, read with --psm 7 and a digit whitelist.
3. Vote per cell over the (up to) 2 cell readings and 3 page readings. A token is read as digits
   with a decimal point after the 1st or 2nd digit (5 digits after the point below 10, 4 above);
   with no usable point, the placement closest to the previous month's value is taken. The most
   common value wins. A cell is flagged when fewer than 3 readings agree, a second value has
   2+ readings, or the move from the previous month exceeds 12% in logs.
4. Every flagged cell (64), plus the full rows 1897-1899 (page 50's worst rows), was read off the
   page image by eye; those values are in `research/results/stale-checks-1-ocr-corrections.csv`
   and override the vote. NYSE closed August-November 1914: those cells are empty.
"""

from __future__ import annotations

import collections
import csv
import json
import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORRECTIONS = HERE.parent / "results" / "stale-checks-1-ocr-corrections.csv"
PAGES = (50, 51)
FIRST, LAST = 1884, 1926
CLOSED = {(1914, k) for k in range(8, 12)}
# left x of the 12 month columns on the rotated 400 dpi page, and the row slope (skew)
COLS = {
    50: (
        [602, 892, 1215, 1508, 1799, 2123, 2406, 2696, 2987, 3309, 3602, 3890],
        (2368 - 2339) / (3890 - 602),
    ),
    51: (
        [543, 835, 1159, 1447, 1739, 2062, 2347, 2636, 2926, 3247, 3542, 3828],
        (1680 - 1727) / (3828 - 543),
    ),
}
YEAR = re.compile(r"(188[4-9]|189\d|19[0-2]\d)")
WL = "tessedit_char_whitelist=0123456789."


def sh(*a: str) -> str:
    return subprocess.run(list(a), check=True, capture_output=True, text=True).stdout


def render(pdf: Path, wd: Path) -> None:
    for r in (300, 400, 500):
        sh(
            "pdftoppm",
            "-r",
            str(r),
            "-f",
            "50",
            "-l",
            "51",
            "-gray",
            "-png",
            str(pdf),
            str(wd / f"p{r}"),
        )
        for p in PAGES:
            src, dst = wd / f"p{r}-{p}.png", wd / f"r-p{r}-{p}.png"
            if r == 500:
                sh("magick", str(src), "-rotate", "90", "-threshold", "60%", str(dst))
                txt = sh("tesseract", str(dst), "-", "--psm", "6", "-c", WL + " ")
            else:
                sh("magick", str(src), "-rotate", "90", str(dst))
                txt = sh("tesseract", str(dst), "-", "--psm", "6")
            (wd / f"r-p{r}-{p}.txt").write_text(txt)


def year_boxes(wd: Path) -> dict[int, tuple[int, int, int]]:
    out = {}
    for p in PAGES:
        tsv = sh("tesseract", str(wd / f"r-p400-{p}.png"), "-", "--psm", "6", "tsv")
        for line in tsv.splitlines()[1:]:
            f = line.split("\t")
            if len(f) >= 12 and YEAR.fullmatch(f[11]) and FIRST <= int(f[11]) <= LAST:
                out[int(f[11])] = (p, int(f[6]), int(f[7]))
    return out


def cell_reads(wd: Path) -> dict[int, list[list[str]]]:
    out: dict[int, list[list[str]]] = {}
    boxes = year_boxes(wd)
    for yr in range(FIRST, LAST + 1):
        p, yx, yy = boxes[yr]
        cols, slope = COLS[p]
        row = []
        for j, cx in enumerate(cols):
            cy = yy + slope * (cx - yx)
            fn, t = wd / f"c{yr}-{j + 1:02d}.png", wd / "t.png"
            sh("magick", str(wd / f"r-p400-{p}.png"), "-crop", f"175x75+{cx - 20}+{int(cy) - 15}",
               "+repage", "-resize", "200%", str(fn))  # fmt: skip
            reads = []
            for th in ("50%", "65%"):
                sh("magick", str(fn), "-threshold", th, str(t))
                reads.append(sh("tesseract", str(t), "-", "--psm", "7", "-c", WL).strip())
            row.append(reads)
        out[yr] = row
    return out


def page_tokens(path: Path) -> dict[int, list[str]]:
    rows = {}
    for line in path.read_text(errors="ignore").splitlines():
        m = re.match(r"^[^0-9]*(188[4-9]|189\d|19[0-2]\d)\s+(.*)$", line.strip())
        if m:
            rows[int(m.group(1))] = [t for t in re.split(r"\s+", m.group(2)) if re.search(r"\d", t)]
    return rows


def norm(t: str, prev: float | None) -> float | None:
    d = re.sub(r"[^0-9.]", "", t)
    if re.fullmatch(r"\d{1,2}\.\d{4,5}", d) and len(d.replace(".", "")) == 6:
        return float(d)
    digits = d.replace(".", "")
    if len(digits) != 6:
        return None
    cands = [float(digits[:1] + "." + digits[1:]), float(digits[:2] + "." + digits[2:])]
    if prev is None:
        return cands[0]
    return min(cands, key=lambda c: abs(math.log(c / prev)))


def vote(
    cells: dict[int, list[list[str]]], pages: list[dict[int, list[str]]]
) -> tuple[dict[int, list[float | None]], list[tuple[int, int]]]:
    res: dict[int, list[float | None]] = {}
    flags = []
    prev = None
    for yr in range(FIRST, LAST + 1):
        vals: list[float | None] = []
        for j in range(12):
            if (yr, j + 1) in CLOSED:
                vals.append(None)
                continue
            reads = list(cells[yr][j])
            for f in pages:
                row = f.get(yr, [])
                if len(row) == 12 or (yr == 1914 and len(row) == 8):
                    reads.append(row[7 if (yr == 1914 and j == 11) else j])
            nums = [n for n in (norm(r, prev) for r in reads) if n is not None]
            c = collections.Counter(nums).most_common()
            best = c[0][0] if c else None
            ok = bool(c) and c[0][1] >= 3 and (len(c) == 1 or c[1][1] <= 1)
            if prev and best and abs(math.log(best / prev)) > 0.12:
                ok = False
            if not ok:
                flags.append((yr, j + 1))
            vals.append(best)
            if best:
                prev = best
        res[yr] = vals
    return res, flags


def corrections(path: Path = CORRECTIONS) -> dict[tuple[int, int], float]:
    with path.open() as f:
        return {(int(r["year"]), int(r["month"])): float(r["value"]) for r in csv.DictReader(f)}


def build(pdf: Path, out: Path, wd: Path) -> list[tuple[int, int]]:
    render(pdf, wd)
    cells = cell_reads(wd)
    pages = [page_tokens(wd / f"r-p{r}-{p}.txt") for r in (300, 400, 500) for p in PAGES]
    res, flags = vote(cells, pages)
    fix = corrections()
    missing = [f for f in flags if f not in fix]
    if missing:
        raise SystemExit(f"flagged cells without an eye-read value: {missing}")
    lines = ["year,month,index"]
    for yr in range(FIRST, LAST + 1):
        for j, x in enumerate(res[yr]):
            v = fix.get((yr, j + 1), x)
            if v is not None:
                lines.append(f"{yr},{j + 1},{v}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n")
    (wd / "flags.json").write_text(json.dumps(flags))
    return flags


def main(argv: list[str]) -> None:
    pdf, out = Path(argv[0]), Path(argv[1])
    if len(argv) > 2:
        wd = Path(argv[2])
        wd.mkdir(parents=True, exist_ok=True)
        flags = build(pdf, out, wd)
    else:
        with tempfile.TemporaryDirectory() as d:
            flags = build(pdf, out, Path(d))
    print(f"wrote {out}; {len(flags)} flagged cells, all overridden from {CORRECTIONS.name}")


if __name__ == "__main__":
    main(sys.argv[1:])
