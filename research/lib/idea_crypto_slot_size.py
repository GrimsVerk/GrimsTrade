"""uv run --with numpy python research/lib/idea_crypto_slot_size.py"""

from datetime import date

import common as c
import rules

IDEA = "crypto-slot-size"
START = date(2013, 1, 1)

if __name__ == "__main__":
    six = c.ctx("six")
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False,
              start=START)  # fmt: skip
    runs = [
        c.go(IDEA, f"c{int(x * 100):02d}", c.weekly(rules.crypto_slot(x)), six, start=START)
        for x in (0.05, 0.10, 0.0)
    ] + [ew]
    out = ["# crypto-slot-size: how big should the crypto slots be?", ""]
    out += ["Card: `cards/crypto-slot-size.md`. Six live assets, decisions from 2013-01-01.", ""]
    out += [c.table(runs, versus=ew), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    out += ["Annualised log growth: " + ", ".join(f"{r.variant} {c.growth(r):+.1%}" for r in runs)]
    c.write_result(IDEA, "\n".join(out))
