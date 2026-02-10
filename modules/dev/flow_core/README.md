# Flow Core

## Overview
Flow Core is a domain-specific language (DSL) compiler for composable AI prompts. It provides tokenization, parsing, and compilation of the Flow language, enabling hierarchical composition of prompt fragments with node references.

**Key Features:**
- Composable prompt fragments with node definitions (`@node`)
- Node references for reuse (`$ref`) and forward references (`^ref`)
- String blocks with trimming (`<<<...>>>`) or whitespace preservation (`<<...>>`)
- File includes and imports

## Features
- **Tokenizer**: Converts Flow source into tokens with line/column tracking
- **Node Definitions**: Define reusable prompt fragments with `@name`
- **References**: Reference other nodes with `$name` or forward-reference with `^name`
- **String Blocks**: Trimmed (`<<<...>>>`) or preserved (`<<...>>`) content blocks
- **File References**: Include external files with `++path`
- **Imports**: Import other Flow files with `+path`
- **Error Reporting**: Line and column tracking for precise error messages

## Token Types

| Token | Trigger | Example |
|-------|---------|---------|
| `COMMENT` | `#` at line start | `# This is a comment` |
| `IMPORT` | `+` at line start | `+./path/to/file.flow` |
| `NODE_DEF` | `@` | `@greeting` |
| `PIPE` | `\|` | Parameter separator |
| `DOT_END` | `\|.` | Node terminator |
| `STRING_TRIM` | `<<<`...`>>>` | Trimmed content |
| `STRING_PRESERVE` | `<<`...`>>` | Preserved whitespace |
| `NODE_REF` | `$id` | `$greeting` |
| `FORWARD_REF` | `^id` | `^greeting` |
| `FILE_REF` | `++path` | `++./doc.md` |
| `ASSIGN` | `=` | `$a.slot = $b` |

## String Modes & Inline Substitution

Flow has two string-block closers that control how adjacent content items are joined during compilation:

| Opener/Closer | Name | Trim? | Join behavior with neighbor |
|---------------|------|-------|-----------------------------|
| `<<<` / `>>>` | Trim | Yes | Newline between items (default) |
| `<<` / `>>` | Preserve | No | **Inline** — no separator |

When the compiler joins content items, it inspects the **closer** of the previous item and the **opener** of the next item. If *either* adjacent boundary is preserve-mode (`<<`/`>>`), the items are concatenated inline (no newline). Otherwise a newline is inserted.

This enables inline substitution — embedding references inside a sentence:

```
@greeting
|<<Hello, >>|$name|<<! Welcome.>>|
|.
```

Compiles to: `Hello, Alice! Welcome.` (assuming `@name` resolves to `Alice`).

The same mechanism works with mixed modes:

```
|<<<First paragraph.>>>|$middle|<<, then inline.>>|
```

Here `<<<...>>>` inserts a newline after "First paragraph." but `<<, then inline.>>` joins inline with `$middle`.

## Usage

```python
from cores.flow_core import Tokenizer, Token, TokenType

# Tokenize Flow source
source = """
@greeting
<<<
Hello, I'm an assistant.
>>>|.
"""

tokenizer = Tokenizer()
tokens = tokenizer.tokenize(source)

for token in tokens:
    print(f"{token.type.name}: {token.value!r}")
```

### CLI Usage

```bash
# Tokenize a Flow file
python -m cores.flow_core.flow_cli tokenize myfile.flow --verbose
```

### Playground

```bash
# Run the tokenizer playground
python -m cores.flow_core.playground.tokenizer_playground
```

## Module Structure

```
flow_core/
├── __init__.py          # Module exports
├── init.yaml            # Module metadata
├── README.md            # This file
├── errors.py            # Error classes (FlowError, TokenizerError)
├── models.py            # Data models (Token, TokenType)
├── tokenizer.py         # Tokenizer implementation
├── flow_controller.py   # Main controller
├── flow_cli.py          # CLI interface
├── refresh.py           # Framework refresh hook
├── tests/               # Unit tests
└── playground/          # Interactive exploration
    └── tokenizer_playground.py
```


## Testing

### Unit Tests (Optional)
```bash
pytest <module_type>/<module_name>/tests/
```

### Adversarial Testing
HyperRed will attack this module based on `testing.scope` in `init.yaml`.
Configure threat_model: `internal` | `external` | `adversarial`