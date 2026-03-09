# Full Skill with Resources

Directory layout for a skill with scripts, references, and assets:

```
my-skill/
├── SKILL.md              # Main instructions
├── scripts/              # Executable code
│   ├── setup.sh.template   # Adding .template to make the IDE stop screaming.
│   └── validate.py         # No need `.template` if it is real executable code, not a template for modification reference.
├── references/           # Additional documentation
│   ├── REFERENCE.md
│   └── api-spec.md
└── assets/               # Static resources
    ├── template.json
    └── schema.yaml
```

## Optional Directories

| Directory | Purpose | Notes |
|-----------|---------|-------|
| `scripts/` | Executable code agents can run | Self-contained, document dependencies |
| `references/` | Additional documentation | Loaded on demand, keep files focused |
| `assets/` | Templates, schemas, data files | Static resources |
