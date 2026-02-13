# 🎯 Indicators Util

> *Calculate technical indicators without fighting pandas indexes*

**Version:** 1.0 | **Status:** ✅ Ready

---

## 📍 What's Here

| Section | Purpose |
|---------|---------|
| [Quick Start](#-quick-start) | Get running in 5 minutes |
| [API Reference](#-api-reference) | Core functions and usage |
| [Edge Cases](#-edge-cases) | Gotchas and known limitations |
| [Upgrade Criteria](#-when-to-upgrade) | When this doc isn't enough |

---

## 🚀 Quick Start

### The 30-Second Version

```python
from indicators_util import calculate_rsi, calculate_macd, calculate_bollinger

# Calculate RSI (default 14 periods)
rsi = calculate_rsi(df['close'])

# Calculate MACD 
macd_line, signal_line, histogram = calculate_macd(df['close'])

# Calculate Bollinger Bands
upper, middle, lower = calculate_bollinger(df['close'])
```

### Step-by-Step Setup

1. **Install dependencies:**
   ```bash
   cd utils/indicators_util
   pip install -r requirements.txt
   ```

2. **Import and use:**
   ```python
   import pandas as pd
   from indicators_util import calculate_rsi
   
   df = pd.read_csv('stock_data.csv')
   df['RSI'] = calculate_rsi(df['close'], period=14)
   ```

### Verify It Works

| Action | Expected Result |
|--------|-----------------|
| `calculate_rsi(pd.Series([1,2,3,4,5]*10))` | Returns Series with RSI values |
| `calculate_macd(prices)` | Returns tuple of 3 Series |

---

## 📚 API Reference

### `calculate_rsi(prices, period=14)`

**Purpose:** Calculate Relative Strength Index

**Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `prices` | `pd.Series` | Required | Close prices |
| `period` | `int` | `14` | Lookback period |

**Returns:** `pd.Series` — RSI values (0-100)

**Example:**
```python
rsi = calculate_rsi(df['close'], period=14)
overbought = df[rsi > 70]
```

---

### `calculate_macd(prices, fast=12, slow=26, signal=9)`

**Purpose:** Calculate MACD indicator components

**Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `prices` | `pd.Series` | Required | Close prices |
| `fast` | `int` | `12` | Fast EMA period |
| `slow` | `int` | `26` | Slow EMA period |
| `signal` | `int` | `9` | Signal line period |

**Returns:** `tuple[pd.Series, pd.Series, pd.Series]` — (macd_line, signal_line, histogram)

---

### `calculate_bollinger(prices, period=20, std_dev=2)`

**Purpose:** Calculate Bollinger Bands

**Returns:** `tuple[pd.Series, pd.Series, pd.Series]` — (upper, middle, lower)

---

## ⚠️ Edge Cases

| Scenario | Behavior | Workaround |
|----------|----------|------------|
| Series shorter than period | Returns NaN for all values | Ensure len(prices) > period |
| NaN values in input | NaN propagates to output | Use `fillna()` before calling |
| Empty Series | Returns empty Series | Check before calling |

---

## 📈 When to Upgrade

**This simple doc works when:**
- ✅ Adding standard indicators (SMA, EMA, RSI, MACD, etc.)
- ✅ Single input → single output pattern
- ✅ No state between calculations

**Upgrade to Blueprint when:**
- ❌ Creating indicator combinations/strategies
- ❌ Adding caching or optimization layers
- ❌ Multiple data sources needed
- ❌ Backtesting integration required

### Auto-Detection Rules (Machine-Readable)

```yaml
upgrade_triggers:
  features_count: ">= 4"
  custom_modules: ">= 3"
  external_apis: ">= 2"
  has_async: true
  multi_user_types: true
```

---

## 📝 Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-22 | Initial indicators: RSI, MACD, Bollinger |
