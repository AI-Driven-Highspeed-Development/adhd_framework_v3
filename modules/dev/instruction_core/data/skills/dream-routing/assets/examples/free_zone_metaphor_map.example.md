# FREE ZONE Example: Metaphor Map

> This example shows how to use analogies to explain complex systems to different audiences. Good metaphors accelerate understanding; bad ones create confusion. Document both.

---

## [Custom] 🎭 Metaphor Map

### For New Users: "The Dashboard Metaphor"

**Metaphor:** Stock indicators are like a car dashboard. You don't need to understand engine thermodynamics to know that "red light = problem."

| Dashboard Element | Stock Equivalent | What It Tells You |
|-------------------|------------------|-------------------|
| Speedometer | Price momentum (rate of change) | How fast is the stock moving? |
| Fuel gauge | RSI | Is the stock running on empty (oversold) or overfilled (overbought)? |
| Temperature warning | Bollinger Band breach | Something unusual is happening, pay attention |
| GPS navigation | Moving averages | Where is the stock heading compared to where it's been? |

**Limitations:** This metaphor breaks down when explaining *why* indicators conflict (your fuel gauge and speedometer don't argue with each other).

---

### For Developers: "The Pipeline Metaphor"

**Metaphor:** Data flows like water through pipes. Each processing stage is a filter or transformer.

```
[Raw OHLCV] → [Validation Pipe] → [Indicator Pipes] → [Signal Aggregation] → [UI Reservoir]
     │              │                    │                    │                   │
   Dirty         Clean out           Feature            Conflicting          Ready for
   data          bad tickers         vectors            signals merged       display
```

**Why This Works:** Developers intuitively understand:
- Pipes can clog (rate limits, API failures)
- Order matters (can't calculate SMA before you have clean data)
- Debugging = finding which pipe is broken

**Limitations:** Doesn't capture that some pipes feed back into earlier stages (e.g., adaptive indicators).

---

### For Stakeholders: "The Weather Forecast Metaphor"

**Metaphor:** Stock indicators are like weather forecasts. They're educated predictions, not guarantees.

| Weather | Stock Analysis |
|---------|----------------|
| "80% chance of rain" | "Strong bearish signals, but could reverse" |
| Short-term vs. long-term forecast | Intraday vs. position trading indicators |
| Multiple weather models disagree | RSI says buy, MACD says wait |
| Forecast accuracy degrades over time | Predictions for next week < predictions for tomorrow |

**Why This Works:** Manages expectations. Nobody sues the weatherman for being wrong.

**Limitations:** Weather doesn't react to forecasts; stocks do (self-fulfilling prophecies when enough traders follow the same signals).

---

### Metaphors We Tried and Abandoned

| Metaphor | Why It Failed |
|----------|---------------|
| "Stocks as sports scores" | Implies there's a winner/loser, encourages zero-sum thinking |
| "Indicators as medical tests" | Too clinical, implies false precision we don't have |
| "Market as casino" | Technically accurate but terrible for user trust |

---

### How to Use This Map

- **Onboarding UI:** Use Dashboard metaphor for tooltips
- **Technical docs:** Use Pipeline metaphor for architecture decisions  
- **Investor/stakeholder meetings:** Use Weather metaphor to set expectations
- **Never mix metaphors in the same conversation** — it confuses more than it helps
