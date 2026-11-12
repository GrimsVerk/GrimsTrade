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
#
# In the job (GITHUB_SHA set) it also refuses to go on unless that commit is the tip of main:
# re-running an old run executes the old commit with its old workflow file and old guards.
set -euo pipefail

BRANCH=paper-trail
if [ -n "${GITHUB_SHA:-}" ]; then
  tip="$(git ls-remote origin refs/heads/main | cut -f1)"
  if [ "$tip" != "$GITHUB_SHA" ]; then
    echo "::error::this run is for commit ${GITHUB_SHA:0:10}, but main is at ${tip:0:10}." \
      "Only the newest code on main writes the record: start the job again, do not re-run." >&2
    exit 1
  fi
fi

# Full ref names: a tag or another branch whose name ends in paper-trail must not be taken.
status=0
git ls-remote --exit-code origin "refs/heads/$BRANCH" >/dev/null 2>&1 || status=$?

if [ "$status" -eq 0 ]; then
  git fetch origin "refs/heads/$BRANCH:refs/heads/$BRANCH"
  git worktree add trail "$BRANCH"
  if [ "$(git -C trail symbolic-ref -q HEAD)" != "refs/heads/$BRANCH" ] ||
    [ "$(git -C trail rev-parse HEAD)" != "$(git rev-parse "refs/heads/$BRANCH")" ]; then
    echo "::error::trail/ is not on the $BRANCH branch (a tag of the same name?)." >&2
    exit 1
  fi
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
