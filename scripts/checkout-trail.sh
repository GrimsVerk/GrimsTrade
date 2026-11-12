#!/usr/bin/env bash
# Check out the record branch (paper-trail) into trail/ for the daily job.
#
#   scripts/checkout-trail.sh            # the branch must exist on origin
#   START_NEW_RECORD=true scripts/checkout-trail.sh
#                                        # ...or, only if origin says it does not exist,
#                                        # start an empty record (first run ever)
#
# A fetch that merely fails (network) or a deleted branch must never silently start a new,
# empty record: the old one would vanish from the scoreboard. So ask the remote first.
set -euo pipefail

BRANCH=paper-trail
status=0
git ls-remote --exit-code --heads origin "$BRANCH" >/dev/null 2>&1 || status=$?

if [ "$status" -eq 0 ]; then
  git fetch origin "$BRANCH:$BRANCH"
  git worktree add trail "$BRANCH"
elif [ "$status" -eq 2 ] && [ "${START_NEW_RECORD:-false}" = "true" ]; then
  echo "origin has no $BRANCH branch: starting a new, empty record (START_NEW_RECORD=true)."
  git worktree add --orphan -b "$BRANCH" trail
elif [ "$status" -eq 2 ]; then
  echo "::error::origin has no $BRANCH branch. If the record was deleted, restore it. If this" \
    "really is the first run, start the workflow by hand with 'start a new record' ticked." >&2
  exit 1
else
  echo "::error::could not reach origin to look for $BRANCH (git ls-remote exit $status);" \
    "not running, so that no new record is started by accident." >&2
  exit 1
fi
