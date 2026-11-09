#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
#
# Tests the Gherkin check of examples/check-features.py (TST-034):
#   - the gherkin-official release matches the pin in requirements.txt;
#   - every feature file in features/ passes the check;
#   - each folder in invalid/ fails it, and the output holds the text that
#     each "# expect:" comment of its files names. A check that accepts a
#     broken file would hide every later error.
#
# Run with the package of requirements.txt installed. Environment: PYTHON
# (default python3, the Python of that install).
set -u
here="$(cd "$(dirname "$0")" && pwd)"
python=${PYTHON:-python3}
fail=0

want=$(sed -n 's/^gherkin-official==\([^ \]*\).*/\1/p' "$here/requirements.txt")
have=$($python -I -c "import importlib.metadata as m; print(m.version('gherkin-official'))" 2>/dev/null)
if [ -z "$want" ] || [ "$have" != "$want" ]; then
  echo "FAIL: gherkin-official ${want:-(no pin in requirements.txt)} is required, found ${have:-none}"; exit 1
fi

check() { $python -I "$here/check-features.py" "$1"; }

if ! out=$(check "$here/features"); then
  echo "FAIL: the example features do not pass the check:"; echo "$out"; fail=1
fi

for dir in "$here"/invalid/*/; do
  dir=${dir%/}
  if out=$(check "$dir"); then
    echo "FAIL: the check accepted the broken fixture $dir"; fail=1; continue
  fi
  while IFS= read -r want; do
    if ! grep -qE -- "$want" <<<"$out"; then
      echo "FAIL: the check rejected $dir, but not for the expected reason: $want"; echo "$out"; fail=1
    fi
  done < <(sed -n 's/^# *expect: *//p' "$dir"/*/*.feature)
done

[ $fail -eq 0 ] && echo "PASS"
exit $fail
