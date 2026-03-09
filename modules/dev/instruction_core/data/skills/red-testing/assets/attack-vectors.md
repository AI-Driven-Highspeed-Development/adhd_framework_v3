# Attack Vectors

Reference tables for common attack patterns by category.

## Boundary Testing

| Target | Attack Vectors |
|--------|---------------|
| Numeric inputs | `0`, `-1`, `MAX_INT`, `float('inf')`, `float('nan')` |
| String inputs | `""`, very long strings (10K+ chars), unicode, null bytes, path traversal |
| Collections | `[]`, `{}`, `None`, single-element, massive collections (100K+ items) |
| File paths | Non-existent, permissions denied, symlinks, special characters |
| Dates/times | Epoch, far-future, timezone edge cases, DST transitions |

## Type Confusion

| Attack | Description |
|--------|-------------|
| Wrong type | Pass `str` where `int` expected, `list` where `dict` expected |
| Subclass substitution | Pass subclass that overrides critical methods |
| Duck-type violation | Object with matching attributes but wrong semantics |
| None injection | Pass `None` for every optional AND required parameter |

## State Attacks

| Attack | Description |
|--------|-------------|
| Double initialization | Call `init()` or `setup()` twice |
| Use-after-close | Call methods after `close()`, `cleanup()`, or context manager exit |
| Concurrent mutation | Modify shared state from multiple threads/coroutines |
| Order violation | Call methods in wrong sequence (read before open, write before connect) |
| Partial failure recovery | Interrupt mid-operation, verify cleanup occurred |

## Error Handling Attacks

| Attack | Description |
|--------|-------------|
| Exception swallowing | Verify errors propagate, not silently caught |
| Error cascade | Trigger error in callback/hook, verify parent handles it |
| Resource leak on error | Force error mid-operation, check file handles/connections closed |
| Retry exhaustion | Exhaust retry limits, verify final error is meaningful |

## Stress Testing

| Attack | Description |
|--------|-------------|
| Rapid-fire calls | Call same function 1000+ times in tight loop |
| Memory pressure | Feed progressively larger inputs until failure |
| Nested depth | Deeply nested structures (100+ levels) |
| Concurrent access | Multiple threads/processes hitting same resource |
