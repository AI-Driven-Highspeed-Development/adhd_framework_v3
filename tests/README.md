# Integration Tests

Cross-module integration tests for the project.

## Structure

```
tests/
├── integration/          # Cross-module workflow tests
│   └── test_*.py
├── conftest.py           # Shared fixtures
└── README.md             # This file
```

## Running Tests

```bash
# From project root with venv activated
pytest tests/
```

## Test Types

| Location | Scope | Purpose |
|----------|-------|---------|
| `<module>/tests/` | Unit | Test module in isolation |
| `tests/integration/` | Integration | Test cross-module workflows |

## HyperRed

Adversarial testing is run per-module via HyperRed agent.
See individual module `init.yaml` for testing scope configuration.
