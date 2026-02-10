# Flow Core Playground

Interactive exploration space for the Flow language tokenizer and parser.

## Purpose

Use this folder for:
- Quick experiments with FLOW syntax
- Demo scripts showing parsing patterns
- Interactive AST exploration
- Testing tokenizer and parser behavior

## Usage

```bash
# From project root with venv activated

# Parse a sample .flow file
python -m cores.flow_core.playground.demo_parse samples/hello.flow

# Parse with verbose tokenizer output
python -m cores.flow_core.playground.demo_parse --verbose samples/nested.flow

# Parse inline FLOW source
python -m cores.flow_core.playground.demo_parse --source '@greeting |<<<Hello!>>>|.'

# Run demo mode (parses all sample files)
python -m cores.flow_core.playground.demo_parse

# Tokenizer exploration
python -m cores.flow_core.playground.tokenizer_playground
```

## Files

- `demo.py` - Basic module demo placeholder
- `demo_parse.py` - Interactive parser exploration with pretty-printed AST
- `tokenizer_playground.py` - Tokenizer exploration and testing
- `compiler_playground.ipynb` - **Jupyter notebook** for interactive compiler testing
- `samples/` - Sample .flow files for testing

## Sample Files

| File | Purpose |
|------|---------|
| `hello.flow` | Simple greeting node - minimal example |
| `nested.flow` | Nested slots and layer calculation |
| `imports.flow` | Import syntax variations |
| `refs.flow` | `$ref`, `^forward`, and `++file` references |
| `complex.flow` | Full-featured example combining all syntax |

## Note

Playground code is NOT production code. It's for exploration only.
