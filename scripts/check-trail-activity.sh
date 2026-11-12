#!/usr/bin/env bash
# The outside witness for the record. Everything inside the paper-trail branch can be rewritten
# by whoever can push to it, commit dates included. GitHub's activity log cannot: it lists every
# push, force-push, deletion and creation of the branch with GitHub's own clock.
#
#   GITHUB_REPOSITORY=owner/name GH_TOKEN=... scripts/check-trail-activity.sh [trail-dir]
#
# Exit 2 if the branch was ever force-pushed, deleted or created twice, or if a commit reached
# GitHub more than MAX_LAG seconds after the time it claims it was made (a back-dated commit:
# decisions count from their commit time, so that time has to be real).
# Exit 0 otherwise; also, with a warning, when GitHub cannot be asked (then nothing was checked).
#
# After the owner has looked at a reported event and accepts it, set the repository variable
# TRAIL_REVIEWED_UNTIL to its timestamp (e.g. 2026-11-12T02:00:00Z): older events are skipped.
set -euo pipefail

TRAIL="${1:-trail}"
REPO="${GITHUB_REPOSITORY:?set GITHUB_REPOSITORY=owner/name}"
BRANCH=paper-trail
REVIEWED_UNTIL="${TRAIL_REVIEWED_UNTIL:-}"
MAX_LAG="${MAX_LAG:-600}"

if ! events="$(gh api --paginate "repos/$REPO/activity?ref=refs/heads/$BRANCH&per_page=100" \
  --jq '.[] | [.timestamp, .activity_type, .actor.login, .before, .after] | @tsv')"; then
  echo "::warning::could not read GitHub's activity log for $BRANCH: rewrite check skipped."
  exit 0
fi

bad=0
creations=0
while IFS=$'\t' read -r stamp kind actor before after; do
  [ -n "$stamp" ] || continue
  if [ -n "$REVIEWED_UNTIL" ] && [[ ! "$stamp" > "$REVIEWED_UNTIL" ]]; then
    continue
  fi
  case "$kind" in
    force_push | branch_deletion)
      echo "::error::$BRANCH: $kind by $actor at $stamp (${before:0:10} -> ${after:0:10})"
      bad=1
      continue
      ;;
    branch_creation) creations=$((creations + 1)) ;;
    push) ;;
    *) continue ;;
  esac
  # Every commit this push brought must have been made shortly before it arrived.
  pushed="$(date -u -d "$stamp" +%s)"
  range="$after"
  [[ "$before" =~ ^0+$ ]] || range="$before..$after"
  while read -r made commit; do
    [ -n "$made" ] || continue
    lag=$((pushed - made))
    if [ "$lag" -gt "$MAX_LAG" ] || [ "$lag" -lt -300 ]; then
      echo "::error::$BRANCH: commit ${commit:0:10} says it was made at" \
        "$(date -u -d "@$made" +%Y-%m-%dT%H:%M:%SZ) but reached GitHub at $stamp (by $actor)"
      bad=1
    fi
  done < <(git -C "$TRAIL" log --format='%ct %H' "$range" 2>/dev/null || true)
done <<<"$events"

if [ "$creations" -gt 1 ]; then
  echo "::error::$BRANCH was created $creations times: it was deleted and started again."
  bad=1
fi
if [ "$bad" -ne 0 ]; then
  echo "The record's history does not match GitHub's log. Not running. See docs/audits/." >&2
  exit 2
fi
echo "GitHub's activity log agrees with the $BRANCH history."
