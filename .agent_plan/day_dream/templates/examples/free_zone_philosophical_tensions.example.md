# FREE ZONE Example: Philosophical Tensions

> This example shows how to document the contradictions and tradeoffs you're actively navigating in a feature design. These aren't "problems to solve" — they're tensions to *manage*.

---

## [Custom] ⚖️ Philosophical Tensions

### Tension 1: Real-Time vs. Accuracy

| Pull Toward Real-Time | Pull Toward Accuracy |
|----------------------|---------------------|
| Users want instant feedback on stock signals | Technical indicators need sufficient data windows |
| Stale data = missed opportunities | Premature signals = false positives = lost trust |
| Competitors show "live" updates | "Live" often means "wrong" in volatile markets |

**Our Position:** Favor accuracy with *perceived* responsiveness. Show processing state ("Calculating 20-day SMA...") rather than fake numbers. Users trust a system that admits it's thinking.

**Validation:** A/B test: Do users prefer instant-but-wrong vs. delayed-but-correct? Hypothesis: Power users prefer accuracy; casual users prefer speed.

---

### Tension 2: Simplicity vs. Power

| Pull Toward Simplicity | Pull Toward Power |
|-----------------------|-------------------|
| New users need 3-click success | Advanced users want 47 configurable parameters |
| Simple UI = fewer support tickets | Power features = competitive moat |
| "Just show me what to buy" | "Let me backtest my custom RSI divergence strategy" |

**Our Position:** Progressive disclosure. P0 is dead simple (3 preset strategies). P1 adds "Advanced" toggle. P2 exposes strategy builder. Never sacrifice the simple path.

**Red Line:** If adding a power feature complicates the simple path, it waits for P2+.

---

### Tension 3: Data Freshness vs. API Costs

| Pull Toward Freshness | Pull Toward Cost Control |
|----------------------|-------------------------|
| Financial data decays fast | yfinance rate limits are real |
| Users expect "current" prices | Caching saves $$ and prevents bans |
| Stale OHLCV = bad indicators | Most indicators work fine on 15-min delayed data |

**Our Position:** Tiered freshness. Real-time for price display (WebSocket when available). 15-min cache for indicator calculation. Daily refresh for historical analysis. Be transparent: show "Data as of 14:32" timestamps.

---

### Living With Tension

These tensions don't resolve — they recur at every decision point. This section exists so future contributors understand *why* we made specific choices, not just *what* we chose.

When in doubt: **Accuracy > Speed**, **Simple Path > Power Features**, **Honest Delays > Fake Freshness**.
