# FREE ZONE Example: Assumption Graveyard

> This example shows how to document the risky assumptions underlying your feature. If any of these are wrong, the feature fails or needs major rework. Each assumption includes an early validation strategy.

---

## [Custom] ⚰️ Assumption Graveyard

### Critical Assumptions (Feature Dies If Wrong)

| Assumption | Risk Level | Why We Believe It | How to Validate Early | Kill Date |
|------------|------------|-------------------|----------------------|-----------|
| yfinance will remain free and accessible | 🔴 HIGH | It's been stable for years | Monitor GitHub issues; have fallback data source identified | P0 must work if yfinance fails |
| Users understand what RSI/MACD mean | 🟡 MEDIUM | Our target users are "informed beginners" | P0 user interview: "What does RSI 70 mean to you?" | Before P1 UI design |
| 15-minute delayed data is acceptable | 🟡 MEDIUM | Day traders aren't our P0 audience | Explicit in onboarding: "This tool is for swing traders" | User feedback in P0 |
| Local SQLite can handle 5 years of daily OHLCV for 500 stocks | 🟢 LOW | ~1.8M rows, <100MB | Prototype benchmark in P0 | Before committing to SQLite |

---

### Convenient Assumptions (We're Not Checking, But Should)

These are things we're *assuming* without evidence, mostly because checking would slow us down. Flag them so future us knows where the bodies are buried.

| Assumption | What If Wrong? | When It Becomes Our Problem |
|------------|----------------|----------------------------|
| Users have stable internet | Offline mode = entire new feature | When we get support tickets about "app doesn't work on train" |
| Stock splits are already adjusted in yfinance data | Indicators calculate wrong; users lose money | When someone notices TSLA indicators are garbage post-split |
| Users run modern browsers (ES6+) | Vis server JS breaks | When we get "syntax error" bug reports |
| UTC timestamps are fine for everyone | Time-based indicators off by hours for international users | When non-US users complain |

---

### Buried Assumptions (We Forgot We Made These)

Added as we discover implicit assumptions hiding in the code:

- *"Empty" assumes no data means user hasn't downloaded yet, not that the ticker is invalid*
- *We assume all tickers use the same exchange hours (9:30-4:00 ET)*
- *Indicator calculations assume no gaps in date sequences*

---

### Validation Cadence

- **Before P0 launch:** Validate all 🔴 HIGH assumptions
- **During P0 user testing:** Validate 🟡 MEDIUM assumptions  
- **P1 planning:** Review this graveyard, move validated items to "Confirmed" section
- **Monthly:** Check if any "Convenient Assumptions" have become actual problems
