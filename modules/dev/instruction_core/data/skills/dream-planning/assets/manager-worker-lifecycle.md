# MANAGER / WORKER Lifecycle

## MANAGER (Processes a Plan)

```
DECOMPOSE  → Verify/create children with _overview.md
DELEGATE   → Assign each child to subagent (max 5 parallel), apply sibling firewall
INTEGRATE  → Collect results, merge outputs, resolve sibling conflicts
REPORT     → Mark plan ✅ [DONE], satisfy closure gates, notify parent
```

| Rule | Detail |
|------|--------|
| MUST create `_overview.md` | If it does not exist |
| MUST NOT fulfill children's tasks | Always delegate |
| MUST integrate | No child output is final until parent accepts |
| MUST satisfy closure gates | State Delta + Module Index + invalidation report |
| Max parallel subagents | 5 |

## WORKER (Fulfills a Task)

```
VALIDATE   → Check magnitude ≠ Epic (refuse + escalate), check dependencies
IMPLEMENT  → Read task spec, create/modify artifacts
VERIFY     → Check acceptance criteria
REPORT     → Mark task ✅ [DONE], notify parent
```

| Rule | Detail |
|------|--------|
| MUST refuse Epic tasks | Escalate to parent for decomposition |
| MUST NOT modify sibling tasks | Or parent plan content |
| MUST report completion | Status marker update to parent |

## Plan Closure Gates

| Gate | Detail |
|------|--------|
| All children resolved | Every child is ✅ DONE or 🚫 CUT |
| State Delta appended | Entry in root `_overview.md` |
| Module Index updated | New modules have BOTH table row AND spec file |
| `last_updated` updated | In plan's frontmatter |
| Invalidations reported | List plans this work compromises |
| Plan archived | Moved to `_completed/YYYY-QN/` |
| `dream validate` passes | Auto-triggered before closure |

## Decomposition Termination

| Becomes a Task when... | Becomes a Plan when... |
|------------------------|----------------------|
| Single agent, single session | Contains ambiguity needing breakdown |
| No ambiguity about output | ≥2 independent children |
| Magnitude ≤ Standard | Magnitude Heavy or Epic |

A plan with only 1 child is suspect — SHOULD flatten. Exception: phase directories (`pNN_`) always stay as directories.
