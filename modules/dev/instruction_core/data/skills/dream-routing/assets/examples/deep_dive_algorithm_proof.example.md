## 🔬 Deep Dive

### Algorithm Analysis: LRU Cache with TTL Support

**Context:** Designing a memory-efficient caching layer for expensive computations (API calls, file parsing, ML inference). The cache must balance hit rate, memory footprint, and stale data eviction.

---

### 1. Problem Definition & Complexity

**Requirements:**
- LRU eviction when capacity reached
- TTL (time-to-live) for automatic expiration
- O(1) get/set operations
- Thread-safe for concurrent access
- Memory-bounded (max N entries OR max M bytes)

**Algorithm Variants Considered:**

| Algorithm | get() | set() | Memory | Thread-Safe | TTL Support |
|-----------|-------|-------|--------|-------------|-------------|
| dict + timestamp | O(1) | O(n)* | O(n) | ❌ | ✅ manual check |
| OrderedDict + move_to_end | O(1) | O(1) | O(n) | ❌ | ✅ with wrapper |
| DLL + HashMap | O(1) | O(1) | O(n) | ✅ with lock | ✅ |
| functools.lru_cache | O(1) | O(1) | O(n) | ✅ | ❌ |
| cachetools.TTLCache | O(1) | O(1) | O(n) | ❌ | ✅ |

*O(n) for eviction scan when full

**Why DLL + HashMap (Chosen Approach):**

The doubly-linked list provides O(1) for:
- **Promotion**: Move accessed node to head
- **Eviction**: Remove tail node
- **Insertion**: Prepend new node at head

HashMap provides O(1) key → node lookup.

```
  HEAD ←→ [A] ←→ [B] ←→ [C] ←→ TAIL
           ↑      ↑      ↑
       HashMap: {"a": A, "b": B, "c": C}
```

---

### 2. Time Complexity Proof

**Claim:** Both `get(key)` and `set(key, value)` are O(1) amortized.

**Proof for `get(key)`:**
1. HashMap lookup: O(1)
2. Check TTL expiration: O(1)
3. If valid, move node to head: O(1) pointer reassignment
4. Return value: O(1)

**Proof for `set(key, value)`:**
1. HashMap lookup to check existence: O(1)
2. If exists: update value + move to head: O(1)
3. If new:
   - Create node: O(1)
   - Insert at head: O(1)
   - HashMap insert: O(1) amortized
   - If over capacity, evict tail: O(1)
4. Total: O(1) amortized

**TTL Expiration Strategy (Lazy vs Active):**

| Strategy | Pros | Cons | When to Use |
|----------|------|------|-------------|
| Lazy (on access) | Zero overhead | Memory not freed until access | Most cases |
| Active (background) | Predictable memory | CPU overhead | Memory-critical |
| Hybrid | Balanced | Complexity | High-throughput systems |

---

### 3. Memory Analysis

**Per-Entry Overhead (Python 3.11, 64-bit):**

| Component | Bytes | Notes |
|-----------|-------|-------|
| DLL Node object | 56 | PyObject header + 3 pointers |
| Key reference | 8 | Pointer to key object |
| Value reference | 8 | Pointer to value object |
| HashMap entry | 24 | Key hash + key ptr + value ptr |
| Timestamp (float) | 24 | For TTL tracking |
| **Total overhead** | **~120** | Plus actual key/value sizes |

**Memory Budget Calculator:**

```python
def max_entries(memory_budget_mb: float, avg_entry_kb: float) -> int:
    """Estimate max cache entries within memory budget."""
    overhead_per_entry = 120  # bytes
    entry_bytes = avg_entry_kb * 1024 + overhead_per_entry
    return int((memory_budget_mb * 1024 * 1024) / entry_bytes)

# Examples:
# 100MB budget, 1KB avg entries → ~87,000 entries
# 100MB budget, 10KB avg entries → ~9,800 entries
```

---

### 4. Thread-Safety Considerations

**Lock Granularity Options:**

| Approach | Read Contention | Write Contention | Complexity |
|----------|----------------|------------------|------------|
| Global lock | High | High | Simple |
| RW lock | Low reads | High writes | Moderate |
| Sharded locks | Low | Low | Complex |
| Lock-free (CAS) | None | None | Very complex |

**Recommendation:** Start with RWLock for P0 (simple, correct). Profile before optimizing.

```python
from threading import RLock

class ThreadSafeLRU:
    def __init__(self, capacity: int, ttl_seconds: float):
        self._lock = RLock()
        self._cache = LRUCache(capacity, ttl_seconds)
    
    def get(self, key: str) -> Any | None:
        with self._lock:
            return self._cache.get(key)
    
    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._cache.set(key, value)
```

---

### 5. Decision Matrix

**When to Use This Pattern:**

| Scenario | Recommended? | Notes |
|----------|--------------|-------|
| Expensive API calls (>100ms) | ✅ Yes | TTL = API cache policy |
| Database query results | ✅ Yes | TTL = data freshness tolerance |
| Static file parsing | ✅ Yes | Long TTL or no TTL |
| ML model inference | ⚠️ Maybe | Consider model versioning |
| User session data | ❌ No | Use Redis/dedicated store |
| Cross-process sharing | ❌ No | In-memory is per-process |

---

### 6. Alternative: Just Use a Library?

**BUY vs BUILD Decision:**

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| `cachetools.TTLCache` | Battle-tested, 50 lines saved | Not thread-safe OOTB | ✅ **Use this + lock wrapper** |
| `functools.lru_cache` | Stdlib, decorator syntax | No TTL, size only | ❌ No TTL |
| `redis` | Distributed, persistent | External dependency | ❌ Overkill for local cache |
| Custom DLL+HashMap | Full control, learning | 100+ lines to maintain | ❌ Unless specific needs |

**Final Recommendation:** `cachetools.TTLCache` with threading.RLock wrapper. Build custom only if you need sharding or async support.
