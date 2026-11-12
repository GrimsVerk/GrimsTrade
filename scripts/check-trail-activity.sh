#!/usr/bin/env bash
# The outside witness for the record. Everything inside the paper-trail branch can be rewritten
# by whoever can push to it, commit dates included. GitHub's activity log cannot: it lists every
# push, force-push, deletion and creation of the branch with GitHub's own clock.
#
#   GITHUB_REPOSITORY=owner/name GH_TOKEN=... scripts/check-trail-activity.sh [trail-dir]
#
# Exit 2 if the branch was ever force-pushed, deleted or created twice, if anyone but the daily
# job (TRAIL_BOT) pushed to it, if a pushed commit is no longer in the record, or if a commit
# reached GitHub more than MAX_LAG seconds after the time it claims it was made (a back-dated
# commit: decisions count from their commit time, so that time has to be real).
# Exit 0 otherwise; also, with a warning, when GitHub cannot be asked (then nothing was checked).
#
# After a person has looked at a reported event and accepts it, they set the repository variable
# TRAIL_REVIEWED_UNTIL to its timestamp (e.g. 2026-11-12T02:00:00Z). Events up to then no longer
# stop the job, but they are not forgotten: they are written to state/acknowledged-rewrites.txt
# in the trail, which the scoreboard prints for good. A date in the future is refused. (Anyone
# with write access can set that variable, so it must never be a silent off-switch.)
set -euo pipefail

TRAIL="${1:-trail}"
REPO="${GITHUB_REPOSITORY:?set GITHUB_REPOSITORY=owner/name}"
BRANCH=paper-trail
REVIEWED_UNTIL="${TRAIL_REVIEWED_UNTIL:-}"
MAX_LAG="${MAX_LAG:-600}"
BOT="${TRAIL_BOT:-github-actions[bot]}"
NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

if [ -n "$REVIEWED_UNTIL" ] && [[ "$REVIEWED_UNTIL" > "$NOW" ]]; then
  echo "::error::TRAIL_REVIEWED_UNTIL ($REVIEWED_UNTIL) is in the future. An acknowledgement" \
    "can only cover events that have already happened."
  exit 2
fi

if ! events="$(gh api --paginate "repos/$REPO/activity?ref=refs/heads/$BRANCH&per_page=100" \
  --jq '.[] | [.timestamp, .activity_type, .actor.login, .before, .after] | @tsv')"; then
  echo "::warning::could not read GitHub's activity log for $BRANCH: rewrite check skipped."
  exit 0
fi
if [ -z "$events" ]; then
  echo "::warning::GitHub's activity log is empty for $BRANCH: nothing was checked."
  exit 0
fi

bad=0
creations=0
new_creations=0
acknowledged=()

# report <reviewed 0|1> <text>: an accepted event is remembered, a new one stops the job.
report() {
  if [ "$1" -eq 1 ]; then
    acknowledged+=("$2")
  else
    echo "::error::$BRANCH: $2"
    bad=1
  fi
}

while IFS=$'\t' read -r stamp kind actor before after; do
  [ -n "$stamp" ] || continue
  reviewed=0
  if [ -n "$REVIEWED_UNTIL" ] && [[ ! "$stamp" > "$REVIEWED_UNTIL" ]]; then
    reviewed=1
  fi
  case "$kind" in
    force_push | branch_deletion)
      report "$reviewed" "$kind by $actor at $stamp"
      continue
      ;;
    branch_creation)
      creations=$((creations + 1))
      [ "$reviewed" -eq 1 ] || new_creations=$((new_creations + 1))
      ;;
    *) ;; # push, pr_merge, merge_queue_merge, and whatever GitHub adds: all bring commits
  esac
  # Only the daily job writes the record. Anyone else's push may be honest; a person must look.
  if [ "$actor" != "$BOT" ]; then
    report "$reviewed" "$kind by $actor at $stamp (only the daily job, $BOT, writes the record)"
  fi
  # What GitHub received must still be part of the record...
  if ! git -C "$TRAIL" merge-base --is-ancestor "$after" HEAD 2>/dev/null; then
    report "$reviewed" "commit ${after:0:10}, which $actor pushed at $stamp, is not in the record"
    continue
  fi
  # ...and every commit this push brought must have been made shortly before it arrived.
  pushed="$(date -u -d "$stamp" +%s)"
  range="$after"
  [[ "$before" =~ ^0+$ ]] || range="$before..$after"
  while read -r made commit; do
    [ -n "$made" ] || continue
    lag=$((pushed - made))
    if [ "$lag" -gt "$MAX_LAG" ] || [ "$lag" -lt -300 ]; then
      report "$reviewed" "commit ${commit:0:10} says it was made at $(date -u -d "@$made" \
        +%Y-%m-%dT%H:%M:%SZ) but reached GitHub at $stamp (by $actor)"
    fi
  done < <(git -C "$TRAIL" log --format='%ct %H' "$range" 2>/dev/null || true)
done <<<"$events"

if [ "$creations" -gt 1 ]; then
  twice="created $creations times: it was deleted and started again"
  if [ "$new_creations" -eq 0 ]; then report 1 "$twice"; else report 0 "$twice"; fi
fi

if [ "$bad" -ne 0 ]; then
  echo "The record's history does not match GitHub's log. Not running. See docs/audits/." >&2
  exit 2
fi

note="$TRAIL/state/acknowledged-rewrites.txt"
if [ "${#acknowledged[@]}" -gt 0 ]; then
  mkdir -p "$TRAIL/state"
  printf '%s\n' "${acknowledged[@]}" >"$note"
  echo "::warning::$BRANCH: ${#acknowledged[@]} rewrite event(s) accepted by" \
    "TRAIL_REVIEWED_UNTIL=$REVIEWED_UNTIL; they stay on the scoreboard."
else
  rm -f "$note"
  echo "GitHub's activity log agrees with the $BRANCH history."
fi
