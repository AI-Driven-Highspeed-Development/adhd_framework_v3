# 99 - References

> Part of [Layered Refresh System Blueprint](./00_index.md)

---

## 🛠️ Core Technologies

| Technology | URL | Purpose |
|------------|-----|---------|
| Python `graphlib` | https://docs.python.org/3/library/graphlib.html | Topological sorting for dependency-aware execution order |

---

## 📖 Documentation

| Topic | URL | Notes |
|-------|-----|-------|
| `graphlib.TopologicalSorter` | https://docs.python.org/3/library/graphlib.html#graphlib.TopologicalSorter | `static_order()` for full ordering, `CycleError` for cycle detection |
| PEP 621 — Project Metadata | https://peps.python.org/pep-0621/ | Standard for `[project] dependencies` in `pyproject.toml` |
| TOML Spec | https://toml.io/en/ | Config format for `pyproject.toml` |

---

## 🔗 Related Projects

| Project | Relationship | URL |
|---------|--------------|-----|
| ADHD Framework `modules_controller_core` | Primary module being modified | Internal: `modules/foundation/modules_controller_core/` |
| ADHD Framework `dependency_walker.py` | Prior art for dependency graph traversal | Internal: `modules/foundation/modules_controller_core/dependency_walker.py` |

---

## 📚 Additional Reading

| Topic | URL |
|-------|-----|
| Topological Sorting (Wikipedia) | https://en.wikipedia.org/wiki/Topological_sorting |
| npm scripts lifecycle | https://docs.npmjs.com/cli/v10/using-npm/scripts | Inspiration for filename-based script conventions |

---

**Prev:** [Implementation](./80_implementation.md)

---

**← Back to:** [Index](./00_index.md)
