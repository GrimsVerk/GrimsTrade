"""uv run --with numpy python research/lib/idea_drawdown_control.py"""

import common as c
import rules
import testkit

if __name__ == "__main__":
    testkit.standard(
        "drawdown-control",
        "drawdown-control: sell gradually into a drawdown",
        {f"d{m}": c.weekly(rules.drawdown_control(m)) for m in (1.0, 1.5)},
        {"sma200": c.weekly(c.slots(c.sma_signal))},
        per_asset=True,
    )
