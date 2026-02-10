# FLOW (Flexible Language for Orchestrating Workflows)

## Introduction to FLOW

FLOW (Flexible Language for Orchestrating Workflows) is a domain-specific language designed to transform prompt engineering from simple text formatting into structured software architecture.

The name reflects the language's core mechanism: treating agent instructions not as static blocks, but as continuous streams of data. It is also deeply inspired by the 'flow state'—that intense period of hyperfocus where ADHD minds find their greatest clarity and productivity. By utilizing a robust pipe-based syntax (|) and an insertion engine capable of infinite nesting, FLOW allows developers to:

Orchestrate complex agent behaviors by composing modular nodes and managing cross-file dependencies.

Flexibly adapt content through distinct lifecycle stages—from authoring and compilation to AI-driven mutation.

Define Workflows where prompts are compiled, validated, and optimized like code, ensuring maintainability for even the most advanced AI systems.

In FLOW, the context doesn't just sit there; it flows.

## Key Features

- **Insertion Engine**: FLOW is basically an insertion engine that allows to insert dynamic content into predefined templates.
- **Modularity and infinite nesting**: FLOW supports modular design and infinite nesting of components, making it easy to build complex prompts from simpler building blocks.
- **Human and LLM Readable**: FLOW is designed to be easily readable and understandable by humans and large language models (LLMs), facilitating collaboration and maintenance.

## Terminology

- **FLOW File**: A file with `.flow` extension containing FLOW code.
- **Node**: A fundamental building block in FLOW, defined by an `@` symbol followed by an identifier and parameters.
- **Parameter**: Key-value pairs that define properties of a node.
- **Content**: The main body of a node, defined within triple angle brackets `<<<>>>` or double angle brackets `<<>>`.

### Time Stage terminology

- **Authoring-time**: The time when the FLOW file is being written or edited by a human or an FLOW file generating AI.
- **Compile-time**: The time when the FLOW file is compiled into the markdown `.md` file.
- **Mutate-time**: The time when the LLM mutates the content of mutable nodes during compilation.
- **Post-mutate compile-time**: The time when the FLOW file with mutated content is re-compiled into the final markdown `.md` file.
- **Usage-time**: The time when the compiled output is used by the agent.

## Basic Syntax

The basic syntax of FLOW consists of nodes, parameters, and content definitions. Here are the fundamental structures:

```flow
@node_id | param1=value1 | param2=value2 |<<<Node content goes here.>>>|.
```

All definitions are id and a chain of parameters separated by `|`, and ending with a period `.`.
Content is not special, it is also a parameter, just not named and have angle brackets to denote string content.

### Minimum node

```flow
@out 
|<<<
Hello
>>>|.
```

Compiles to:

```
Hello
```

Or:

```flow
@out 
|<<
Hello
>>|.
```

Compiles to:

```

Hello

```

only @out node is required in a FLOW file. Other nodes are optional and can be defined as needed.

#### The `@` Symbol
The `@` symbol is used to define nodes in FLOW. Each node can have an identifier (name) and optional parameters.

#### The `|` Pipe Symbol
The `|` pipe symbol is used to separate different parts of a node definition, such as the node identifier, parameters, and content.

#### String Blocks: `<<<` / `<<` Openers and `>>>` / `>>` Closers
FLOW has two string *openers* and two string *closers*:

- Openers: `<<<` (trim mode) and `<<` (preserve mode)
- Closers: `>>>` (trim mode) and `>>` (preserve mode)

**Asymmetric pairing is allowed**: `<<<` may close with either `>>>` **or** `>>`, and `<<` may close with either `>>` **or** `>>>`.

The *opener* controls the start of the string block, while the *closer* controls the end of the string block.

- `<<<...` (trim mode): leading line breaks are trimmed
- `<<...` (preserve mode): leading whitespace and line breaks are preserved
- `...>>>` (trim mode): trailing line breaks are trimmed
- `...>>` (preserve mode): trailing whitespace and line breaks are preserved

This means all of these are valid and equivalent in terms of closing delimiter choice:

```flow
@a |<<<

Hello

>>|.

@out 
|$a
```

Compiles to:

```
Hello


```

And:

```flow
@b |<<

Hello

>>>|.

@out 
|$b
```

Compiles to:

```


Hello
```

#### The `.` Period Symbol
The period symbol at the end of a node definition indicates the end of that node.

---

### Node with id name

```flow
@greeting 
|<<<
Hello! How can I assist you today?
>>>|.

@out |$greeting|.
```

Compiles to:

```
Hello! How can I assist you today?
```

Where `greeting` is the identifier for this node. and can be referenced elsewhere in the FLOW file using `$greeting`.

### The `$` Symbol
The `$` symbol is used to reference nodes and their content within other nodes. It allows for dynamic insertion of content. The referenced node must be defined before it is referenced, position-wise.

#### `$name` is Literal Inside Content Blocks

Inside `<<<>>>` or `<<>>` content blocks, `$name` is treated as **literal text**, not a reference. To insert a node reference within content, you must close the content block with `>>>|`, add the reference `|$ref|`, and optionally continue with another content block:

```flow
@greeting |<<<Hello!>>>|.

@out 
|<<<Welcome! >>|$greeting|<< How are you?>>>|.
```

Compiles to:

```
Welcome! Hello! How are you?
```

The pattern is: `|<<<text>>|$ref|<<more text>>>|.`

### The `^` Symbol (Forward References)

The `^` symbol is used to reference nodes that will be defined **later** in the file (below the current position). This is the counterpart to `$` which requires the node to be defined above.

| Symbol | Meaning | When to Use |
|--------|---------|-------------|
| `$name` | Backward reference | Node is defined above (already parsed) |
| `^name` | Forward reference | Node will be defined below (not yet parsed) |

```flow
@out 
|<<<Intro: >>|^greeting|.

@greeting 
|<<<Hello, World!>>>|.
```

Compiles to:

```
Intro: Hello, World!
```

#### Forward Reference Validation

- Forward references (`^name`) are validated during **Stage 3 (Resolution)**, not during parsing
- If a forward reference points to a node that is never defined, an `UndefinedNodeError` is raised
- **Cycle detection still applies**: `^a` → `$b` → `^a` is a circular dependency error

---

### Node with parameters

```flow
@farewell 
|style.title=<<Goodbye>>
|<<<
Have a great day!
>>>|.
```

Compiles to:

```
# Goodbye
Have a great day!
```

Where `style.title` sets the title of the node.

#### String in parameter

Consider the content strings is a parameter without a name, `style.title` is just a string parameter with a name.

### Predefined Parameters

- `style`: a predefined parameter group can include various styling options, current it only have `title`. (which will be introduced later)

---
### Node with insertion

Assuming the above two nodes are not defined yet, here is a fresh example:

```flow
@main_message 
|@greeting |.
|@farewell | style.title=<<See you later!>> |.
|.

@greeting 
|<<<
Hello! How can I assist you today?
>>>|.

@farewell 
|style.title=<<Goodbye>> 
|<<<
Have a great day!
>>>|.

$main_message.greeting = $greeting
$main_message.farewell = $farewell

@out 
|<<<
$main_message
>>>|.
```

Compiles to:

```
Hello! How can I assist you today?
# Goodbye
Have a great day!
```

#### The `=` Equal Symbol
The `=` equal symbol is used to assign the referenced node to another node. **Assignment creates an independent deep copy of the node**, not a reference. In this case, the `$greeting` node is copied to the `main_message.greeting` slot, and the `$farewell` node is copied to the `main_message.farewell` slot.

The `main_message.greeting` and `main_message.farewell` are declared during the declaration of `@main_message` node.

#### Referencing the newly defined nodes

Note that the line "# See you later!" is not included in the final output because the original node `$main_message.farewell` slot is replaced by a deep copy of the `$farewell` node with the title "Goodbye".

**Deep copy semantics** (similar to Python's `copy.deepcopy`):

```python
import copy

class Example:
    def __init__(self):
        self.content = "Original"

template = Example()
template.content = "Template Content"

# Assignment creates an independent copy
slot = copy.deepcopy(template)
slot.content = "Modified"  # Does NOT affect the original template

print(template.content)  # Output: "Template Content" (unchanged)
print(slot.content)      # Output: "Modified"
```

This means modifications to the assigned node do not affect the source node, and vice versa.

---

### Comment

```flow
# This is a comment line in FLOW
@out 
|<<<
Hello, World!
>>>|.
```

Compiles to:

```
Hello, World!
```

Cannot use `#` inside `<<>>` or `<<<>>>`, because it will be treated as normal content.

```flow
@out
|<<<
# This is not a comment, it's part of the content.
>>>|.
```

Compiles to:

```
# This is not a comment, it's part of the content.
```

---

### Importing Nodes from other FLOW files
You can import nodes from other FLOW files using the `+` symbol.

```flow
# In other_file.flow

@external_node 
|<<<
This content is from another FLOW file.
>>>|.
```

```flow
+./path/to/other_file.flow |.

@out 
|<<<
$external_node
>>>|.
```

Compiles to:

```
This content is from another FLOW file.
```

#### Importing Specific Nodes

Or, you can import specific nodes:

```flow
# In other_file.flow

@external_node 
|<<<
This content is from another FLOW file.
>>>|.

@another_node 
|<<<
This is another node from the same FLOW file.
>>>|.

@yet_another_node 
|<<<
This node will not be imported.
>>>|.
```

```flow
+./path/to/other_file.flow | $external_node | $another_node |.

@out 
|$external_node 
|$another_node
|.
```

Compiles to:

```
This content is from another FLOW file.
This is another node from the same FLOW file.
```

#### Renaming Imported Nodes 

To prevent naming conflicts, you can rename imported nodes:

```flow
# In other_file.flow
@external_node 
|<<<
This content is from another FLOW file.
>>>|.

@another_node 
|<<<
This is another node from the same FLOW file.
>>>|.
```

```flow
+./path/to/other_file.flow 
|@first_outer_node|. = $external_node
|@second_outer_node|. = $another_node
|.

@out 
|$first_outer_node
|$second_outer_node
|.
```

Compiles to:

```
This content is from another FLOW file.
This is another node from the same FLOW file.
```

#### The `+` Plus Symbol
The `+` plus symbol is used to import other FLOW files.

#### External `out` Node
The `out` node in the imported FLOW file will be ignored during the import process. For both the all-nodes import and specific-nodes import.

---

### Referring to specific files

One of the benefits of FLOW is that you can explicitly refer to specific files, then the compiler can catch it and later create a tree diagram of all the FLOW files and their dependencies:

```flow
@workflow 
|<<<
To complete this task, please refer to the instructions in the file: >>|++./path/to/specific_file.md|<<
In the file, you will find detailed steps and guidelines to follow.
>>>|. 

@out 
|<<<
$workflow
>>>|.
```

Compiles to:

```
To complete this task, please refer to the instructions in the file: ./path/to/specific_file.md
In the file, you will find detailed steps and guidelines to follow.
```

As you can see, the `++` did not do anything special during compilation, but it tells the compiler that this is a specific file reference, not an import.

But it can:
1. Let the compiler validate that the file exists at the specified path. (After compilation and deployment, because during compilation the file may not exist yet.)
2. Record the file reference in the dependency graph for the FLOW file.
3. The graph can be used later for visualization, analysis, or optimization of the FLOW file structure.
4. Or even a guide for FLOW writing AI agents to navigate and understand the instructions across multiple files.

---

### Escape
To include literal `|` in your content, you can escape them using a backslash `\`.
But the case you need to escape is extremely rare, because most of the symbols needs to pair with a pipe `|`, and `|` without other symbols is meaningless in FLOW.

```flow
@out 
|<<<
This is a literal closing angle bracket with pipe: >>>\| string not stopped
This is a literal at symbol: >>>\|@not_a_node
This no need to escape: 
    @not_a_node 
    >>> string not stopped 
    | pipe alone without the ending >>> also just text
    |. pipe with dot ending but still before >>> is also just text
    +this/path/do/not/import because it is still in the string block
>>> 
|.
```

Compiles to:

```
This is a literal closing angle bracket with pipe: >>>| string not stopped
This is a literal at symbol: >>>|@not_a_node
This no need to escape: 
    @not_a_node 
    >>> string not stopped
    | pipe alone without the ending >>> also just text
    |. pipe with dot ending but still before >>> is also just text
    +this/path/do/not/import because it is still in the string block
```

#### `|` Pipe after escaped symbols
There is only one case I can think of that you need to escape a `|` pipe symbol, which is when it is right after a `>>>` or a `>>` closing angle bracket. There for the syntax is extremly robust and rarely need escaping.

---

### Inplace definition without insertion

I don't know why you would want to do this, but by definition of FLOW, you can do this:

```flow
@out

|@greeting | style.title=<<Hello there!>> 
|<<<
Hello! How can I assist you today?
>>>|.

|@farewell | style.title=<<See you later!>> |
<<<
Have a great day!
>>>|. 
 
|.
```

Compiles to:

```
# Hello there!
Hello! How can I assist you today?

# See you later!
Have a great day!
```

---

### Mutable and Remutate Nodes

```flow
@dynamic_content | mutable=true | remutate=true 
|llm_strategy.instruction=<<Generate a creative greeting message.>>
|<<<
[Place holder for a greeting message.]
>>>|.

@out
|<<<
$dynamic_content
>>>|.
```

#### Compilation Process

Compiles to a node that can be altered by the LLM compiler each time it is compiled. The `llm_strategy.instruction` parameter provides guidance to the LLM on how to modify the content.

#### Stage 1 - Compile-time

The 1st stage compilation complies the FLOW file as normal, producing the initial content:

```
[Place holder for a greeting message.]
```

#### Stage 2 - Mutate-time

The 2nd stage compilation happen on the .flow file:

```flow
@dynamic_content | mutable=true | remutate=false 
|llm_strategy.instruction=<<Generate a creative greeting message.>>
|<<<
Howdy! What'up bro!
>>>|.

@out
|<<<
$dynamic_content
>>>|.
```

#### Stage 3 - Post-mutate compile-time

The 3rd stage compilation happen as normal, notice that the `remutate` parameter is set to `false` automatically after the 1st stage compilation to prevent further mutations in subsequent compilations.

```
Howdy! What'up bro!
```

#### LLM Context:

The LLM compiler will be provided with the following context when processing mutable nodes:
- The output of 1st stage compilation.
- The `llm_strategy.instruction` parameter to guide the content modification.
- The full FLOW file content to understand the overall structure and context.

---

### Mimic case-switch

At usage-time, we can instruct the agent to choose different branches based on conditions. It is not in compile-time, so it is just a output telling the agent what to do.

```flow
@condition_check 
|<<<
If the user ask for "discussion" or any similar terms, read>>| ++./discussion_guide.md |<<
If the user ask for "summary" or any similar terms, read>>| ++./summary_guide.md |<<
Otherwise, read>>| ++./default_guide.md |.

@out 
|<<<
$condition_check
>>>|.
```

Or even more structured:

```flow
# style.format did not exist yet, but get along with the vibe first.

@discussion_def | style.format=<<numbered_list>>
|<<<
discussion mode: If the user ask for "discussion" or any similar terms.
please follow: >>| [@target_path|.]
|.

@implementation_def | style.format=<<numbered_list>>
|<<<
implementation mode: If the user ask for "implementation" or any similar terms.
please follow: >>| [@target_path|.]
|.

$discussion_def.target_path = @_|++./discussion_guide.md|.
$implementation_def.target_path = @_|++./summary_guide.md|.

@condition_def
|$discussion_def
|$implementation_def
|<<<
Otherwise, read>>| ++./default_guide.md |<<
>>>|.

@out 
|<<<
$condition_def
>>>|.
```

Compiles to:

```
discussion mode: If the user ask for "discussion" or any similar terms.
please follow: ./discussion_guide.md
implementation mode: If the user ask for "implementation" or any similar terms.
please follow: ./summary_guide.md
Otherwise, read ./default_guide.md
```

#### `@_|` Anonymous Node Definition
You can define an anonymous node (node without a user-specified id) by using `@_|` syntax. This is useful for temporary or one-time use nodes that do not need to be referenced elsewhere.

**Deterministic ID Generation**: Anonymous nodes are assigned a deterministic internal ID based on a hash of their position (file path + line number) and content. This ensures:
- Reproducible compilation across runs
- Stable references in error messages
- Predictable behavior for debugging

**Syntax examples**:
- `@_|++./path|.` — Anonymous node with file reference
- `@_|<<<content>>>|.` — Anonymous node with content
- `@_|.` — Empty anonymous node (valid but rarely useful)

Note that the final id of `$discussion_def.target_path` and `$implementation_def.target_path` are still their original slot ids. The `=` assigns a deep copy but preserves the slot's original id, because our `id` is an artificial identifier that is not like real address references in memory.

---

## The parsing and compilation process

The parsing will be done in python.

### FLOW of FLOW

1. parse with a state machine, in recursive manner.
2. all spaces, line breaks, indentations outside of `<<<>>>` or `<<>>` are ignored.

## Node definition

```python
import re
from dataclasses import dataclass
from typing import List, Union
from pathlib import Path

@dataclass
class FlowNode:
    id: str = None
    params: FlowParams = None
    layer: int = 0 # depth layer of the node in the tree
    refered_paths: List[Path] = None # list of Path objects for referred files
    content: List[Union[str, FlowNode]] = None # content can be a list of strings and nested FlowNode objects

@dataclass
class FlowParams:
    style: FlowStyle = None
    llm_strategy: FlowLLMStrategy = None
    mutable: bool = False # `mutable` set it to True,
    remutate: bool = False # `remutate` set it to True, 

    # Only the node with both `mutable` and `remutate` set to True will be re-mutated by LLM at each compilation, then the `remutate` parameter will be set to False automatically after the first re-mutation.

@dataclass
class FlowStyle:
    title: str = None
    # will add more later

@dataclass
class FlowLLMStrategy:
    instruction: str = None
    # will add more later
```
    
## Compilation Steps

The compilation process follows a multi-stage pipeline: **Tokenize → Parse → Resolve → Compile → (Optional) LLM Mutate**.

---

### Stage 1: Tokenization

Scan the source file character-by-character, producing tokens:

| Token Type | Trigger | Description |
|------------|---------|-------------|
| `COMMENT` | `#` at line start | Entire line ignored |
| `IMPORT` | `+` at line start | File import statement |
| `NODE_DEF` | `@` | Node definition start |
| `ANON_NODE_DEF` | `@_` | Anonymous node definition start |
| `PIPE` | `\|` | Parameter/section separator |
| `DOT_END` | `\|.` | Node definition terminator |
| `STRING_TRIM` | `<<<` ... (`>>>` or `>>`) | String content (trim leading/trailing newlines) |
| `STRING_PRESERVE` | `<<` ... (`>>` or `>>>`) | String content (preserve all whitespace) |
| `NODE_REF` | `$identifier` | Reference to another node (must be defined above) |
| `FORWARD_REF` | `^identifier` | Forward reference to a node (will be defined below) |
| `FILE_REF` | `++path` | Explicit file path reference |
| `ASSIGN` | `=` | Assignment operator |

**Escape handling**: `\|` within string blocks produces a literal `|`.

---

### Stage 2: Parsing (Recursive Descent)

Build an AST from the token stream:

```
FlowFile
├── imports: List[ImportNode]
├── nodes: Dict[str, FlowNode]
└── assignments: List[AssignmentNode]
```

### 2.1 Parse Imports

```
+./path/to/file.flow |.                    # Import all nodes
+./path/to/file.flow | $node1 | $node2 |.  # Import specific nodes
+./path/to/file.flow | @alias|. = $original |.  # Import with rename
```

- Recursively parse imported files
- Merge imported nodes into current namespace (skip external `@out` nodes)
- Handle renames to avoid conflicts

#### 2.2 Parse Node Definitions

For each `@` token:

1. **Read node ID**: Characters until `|` or end of line
2. **Parse parameters**: Key-value pairs separated by `|`
   - Named params: `key=<<value>>` or `key=value`
   - Unnamed content: `<<<...>>>` or `<<...>>`
3. **Parse nested nodes**: Inner `@node |...|.` within the parameter list
4. **Terminate on `|.`**: Signals end of node definition

#### 2.3 Parse Assignments

```
$parent.slot = $child
```

- Left-hand side: Dotted path to insertion slot
- Right-hand side: Node reference to insert

---

### Stage 3: Resolution

Resolve all references and build the final node graph:

1. **Validate backward references**: Ensure all `$identifier` point to nodes defined above
2. **Validate forward references**: Ensure all `^identifier` point to nodes defined anywhere in the file
3. **Apply assignments**: Replace insertion slots with deep copies of referenced nodes
4. **Validate file references**: Record all `++path` references for dependency graph
5. **Cycle detection**: Error if circular dependencies exist (applies to both `$` and `^` references)

---

### Stage 4: Compilation

Starting from `@out`, recursively compile to output string:

```python
def compile_node(node: FlowNode, style_registry: StyleRegistry) -> str:
    result = []
    
    # Phase 1: Apply pre-content styles (e.g., titles, headers)
    if node.params and node.params.style:
        pre_content = style_registry.apply_pre(node.params.style, node.layer)
        if pre_content:
            result.append(pre_content)
    
    # Phase 2: Process content list
    for item in node.content:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, FlowNode):
            # Nested nodes inherit layer + 1 for heading depth
            result.append(compile_node(item, style_registry))
    
    # Phase 3: Apply post-content styles (e.g., dividers, closers)
    if node.params and node.params.style:
        post_content = style_registry.apply_post(node.params.style, node.layer)
        if post_content:
            result.append(post_content)
    
    # Phase 4: Apply wrap styles (e.g., blockquote, code fence)
    compiled = "\n".join(result)
    if node.params and node.params.style:
        compiled = style_registry.apply_wrap(node.params.style, compiled, node.layer)
    
    return compiled
```

#### Layer-Aware Heading

The `node.layer` field determines heading depth for styles that produce markdown headings:

| Layer | Heading Output |
|-------|----------------|
| 0 | `#` (H1) |
| 1 | `##` (H2) |
| 2 | `###` (H3) |
| ... | ... |

#### Style Registry (Separate Concern)

Styles are processed through a pluggable `StyleRegistry`. Each style handler implements:

```python
class StyleHandler(Protocol):
    def apply_pre(self, style: FlowStyle, layer: int) -> str | None:
        """Content to prepend (e.g., heading, opening tag)"""
        ...
    
    def apply_post(self, style: FlowStyle, layer: int) -> str | None:
        """Content to append (e.g., divider, closing tag)"""
        ...
    
    def apply_wrap(self, style: FlowStyle, content: str, layer: int) -> str:
        """Transform the entire compiled content (e.g., indent, fence)"""
        ...
```

**Example handlers** (defined separately, not in compilation logic):

| Style | Phase | Transformation |
|-------|-------|----------------|
| `style.title` | `pre` | `"#" * (layer + 1) + " " + title` |
| `style.divider` | `post` | `"---"` |
| `style.blockquote` | `wrap` | Prefix each line with `> ` |
| `style.codefence` | `wrap` | Wrap in ` ``` ` blocks |

**Compilation rules**:
- Concatenate string content in order
- Recursively compile nested `FlowNode` objects (incrementing layer)
- Delegate all style transformations to `StyleRegistry`
- Trim vs preserve whitespace based on `<<<>>>` vs `<<>>`

---

### Stage 5: LLM Mutation (Optional)

For nodes with `mutable=true` AND `remutate=true`:

1. **Collect context**:
   - Stage 4 output (current compiled content)
   - `llm_strategy.instruction` parameter
   - Full FLOW file for structural context

2. **Send to LLM**: Request content modification per instruction

3. **Update source**: Replace node content in `.flow` file, set `remutate=false`

4. **Recompile**: Run Stage 4 again with mutated content

---

#### State Machine Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        IDLE                                     │
│  Wait for: # (comment) | + (import) | @ (node) | $ (assign)     │
└─────────────────────────────────────────────────────────────────┘
       │           │            │              │
       ▼           ▼            ▼              ▼
   ┌───────┐  ┌────────┐  ┌──────────┐  ┌────────────┐
   │COMMENT│  │ IMPORT │  │NODE_DEF  │  │ ASSIGNMENT │
   │skip ln│  │parse   │  │parse id  │  │ $a.b = $c  │
   └───────┘  │path,   │  │params,   │  └────────────┘
              │nodes   │  │content   │
              └────────┘  └──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
              ┌──────────┐          ┌──────────┐
              │ PARAMS   │          │ CONTENT  │
              │ key=val  │◄────────►│ <<<...>>>│
              │ nested @ │          │ $refs    │
              └──────────┘          └──────────┘
                    │
                    ▼
              ┌──────────┐
              │  |. END  │ ──► back to IDLE
              └──────────┘
```

---

#### Error Handling

| Error | Trigger | Message |
|-------|---------|---------|
| `UndefinedNodeError` | `$foo` where `@foo` not defined | `Node '$foo' referenced but not defined` |
| `CircularDependencyError` | `$a` contains `$b` contains `$a` | `Circular dependency detected: a → b → a` |
| `UnclosedStringError` | `<<<` without matching `>>>` | `Unclosed string block starting at line N` |
| `InvalidImportError` | `+path` file not found | `Cannot import: file 'path' not found` |
| `DuplicateNodeError` | Two `@foo` definitions | `Duplicate node definition: 'foo'` |

