#!/usr/bin/env bash
# May today's intraday collection run and be saved to the Actions cache? Writes `ok=yes` or
# `ok=no` to $GITHUB_OUTPUT (stdout when unset). Never fails the job.
#
# The store is an Actions cache (not public; docs/DECISIONS.md). Each run restores the newest
# `intraday-*` entry and saves a new one. The danger is a restore that misses while a store
# exists: the run would then save a short, fresh copy that becomes the newest entry, and the
# next restore would pick it, dropping days the sources no longer serve. So:
#   restored (MATCHED_KEY set)            -> ok=yes
#   nothing restored, no store exists yet -> ok=yes (start one)
#   nothing restored, a store exists      -> ok=no  (skip today; the old store stays newest)
#   GitHub can't be asked                 -> ok=no
# Needs `gh` with GH_TOKEN (actions: read).
set -u
out="${GITHUB_OUTPUT:-/dev/stdout}"
matched="${MATCHED_KEY:-}"
repo_args=()
if [ -n "${GITHUB_REPOSITORY:-}" ]; then repo_args=(--repo "$GITHUB_REPOSITORY"); fi

if [ -n "$matched" ]; then
  echo "Restored the intraday store from $matched."
  echo "ok=yes" >>"$out"
  exit 0
fi
if ! count=$(gh cache list "${repo_args[@]}" --key intraday- --limit 1 --json key --jq length); then
  echo "::warning::Could not ask GitHub whether an intraday store exists; not collecting today."
  echo "ok=no" >>"$out"
  exit 0
fi
if [ "$count" = "0" ]; then
  echo "No intraday store yet: starting one."
  echo "ok=yes" >>"$out"
  exit 0
fi
echo "::warning::An intraday store exists but did not restore; not collecting today, so no shorter copy replaces it."
echo "ok=no" >>"$out"
