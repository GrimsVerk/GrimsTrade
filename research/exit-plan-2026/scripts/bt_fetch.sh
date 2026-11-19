#!/usr/bin/env bash
# Refresh daily bars from Yahoo's public chart endpoint into a scratch dir (never committed).
# Usage: bt_fetch.sh <out_dir>
set -euo pipefail
out="$1"
mkdir -p "$out"
now=$(date +%s)
for sym in '^GSPC' '^IXIC' '^VIX' '^VIX3M' HYG LQD OSEBX.OL '^OSEAX' OBX.OL EQNR.OL NVDA '^SOX' XLK; do
  enc=${sym//^/%5E}
  curl -sS --max-time 60 -A 'Mozilla/5.0 (research script)' \
    -o "$out/$sym.json" \
    "https://query1.finance.yahoo.com/v8/finance/chart/$enc?period1=-1325635200&period2=$now&interval=1d&includeAdjustedClose=true" \
    || echo "failed $sym"
  sleep 1
done
ls -la "$out"
