"""
Flow Core Data Models

Defines token types, token dataclass, and AST nodes for the Flow language.
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Union


# =============================================================================
# Token Types and Token (Tokenizer output)
# =============================================================================


class TokenType(Enum):
    """Token types recognized by the Flow language tokenizer."""
    
    # Comments and imports
    COMMENT = auto()       # # at line start
    IMPORT = auto()        # + at line start (e.g., +./path/to/file.flow)
    
    # Node definitions and references
    NODE_DEF = auto()      # @ (e.g., @greeting)
    NODE_REF = auto()      # $id (e.g., $greeting)
    FORWARD_REF = auto()   # ^id (e.g., ^greeting)
    
    # File references
    FILE_REF = auto()      # ++path (e.g., ++./doc.md)
    
    # Operators
    PIPE = auto()          # | - parameter separator
    DOT_END = auto()       # |. - node terminator
    ASSIGN = auto()        # = - assignment operator
    
    # String blocks
    STRING_TRIM = auto()     # <<<...>>> or <<<...>> (trimmed content)
    STRING_PRESERVE = auto() # <<...>> or <<...>>> (preserved whitespace)
    
    # Identifiers and misc
    IDENTIFIER = auto()    # General identifier
    PARAM_NAME = auto()    # Parameter name in node definition
    
    # End of file
    EOF = auto()


@dataclass
class Token:
    """
    Represents a single token from the Flow language source.
    
    Attributes:
        type: The type of token (from TokenType enum)
        value: The string value of the token
        line: 1-based line number where token appears
        column: 1-based column number where token starts
        closer_trim: For string tokens, True if closer was >>> (trim),
                     False if closer was >> (preserve), None otherwise.
    """
    type: TokenType
    value: str
    line: int
    column: int
    closer_trim: Optional[bool] = None
    
    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"


# =============================================================================
# AST Nodes (Parser output)
# =============================================================================


@dataclass
class Position:
    """
    Source location for error reporting.
    
    Attributes:
        line: 1-based line number
        column: 1-based column number
    """
    line: int
    column: int
    
    def __repr__(self) -> str:
        return f"Position(line={self.line}, col={self.column})"


@dataclass
class FlowStyle:
    """
    Style parameters for a node.
    
    Attributes:
        title: Optional title that becomes a markdown heading
        divider: Whether to emit a horizontal rule after content
        list_type: List formatting type ('bullet', 'numbered', 'task', 'task-done')
        wrap: Wrapper type ('xml', 'codeblock', 'blockquote', 'details')
        tag: For xml: tag name. For codeblock: language identifier
        summary: For details: summary text shown in collapsed state
        level: Absolute heading level (1-6) for style.title, overrides layer
        level_offset: Relative offset to add to layer-based heading level
    """
    title: Optional[str] = None
    divider: bool = False
    list_type: Optional[str] = None  # 'bullet', 'numbered', 'task', 'task-done'
    # Wrapper styles
    wrap: Optional[str] = None       # 'xml', 'codeblock', 'blockquote', 'details'
    tag: Optional[str] = None        # For xml: tag name. For codeblock: language
    summary: Optional[str] = None    # For details: summary text
    # Heading level control
    level: Optional[int] = None      # Absolute heading level (1-6)
    level_offset: Optional[int] = None  # Relative offset (+N adds to layer)


@dataclass
class FlowLLMStrategy:
    """
    LLM mutation strategy parameters.
    
    Attributes:
        instruction: Guidance for LLM content modification
    """
    instruction: Optional[str] = None


@dataclass
class FlowParams:
    """
    Parameters for a FlowNode.
    
    Attributes:
        style: Style parameters (title, etc.)
        llm_strategy: LLM mutation strategy
        mutable: Whether the node can be mutated by LLM
        remutate: Whether to re-mutate on each compilation
    """
    style: Optional[FlowStyle] = None
    llm_strategy: Optional[FlowLLMStrategy] = None
    mutable: bool = False
    remutate: bool = False


@dataclass
class NodeRef:
    """
    Reference to another node ($id or $id.slot).
    
    Attributes:
        id: The full identifier (e.g., "greeting" or "main.slot")
        is_forward: True if this is a forward reference (^id)
        position: Source location for error reporting
    """
    id: str
    is_forward: bool = False
    position: Optional[Position] = None
    
    def __repr__(self) -> str:
        prefix = "^" if self.is_forward else "$"
        return f"NodeRef({prefix}{self.id})"


@dataclass
class FileRef:
    """
    Reference to an external file (++path).
    
    Attributes:
        path: The file path
        position: Source location for error reporting
    """
    path: str
    position: Optional[Position] = None
    
    def __repr__(self) -> str:
        return f"FileRef(++{self.path})"


class StringContent(str):
    """
    String subclass carrying inline-join metadata for boundary-aware joining.
    
    Since str is immutable, metadata is set via __new__.
    isinstance(x, str) returns True, and equality (x == "Hello") works normally.
    
    Attributes:
        opener_trim: True if opener was <<< (trim), False if << (preserve), None if unknown.
        closer_trim: True if closer was >>> (trim), False if >> (preserve), None if unknown.
    """
    
    def __new__(
        cls,
        value: str = "",
        *,
        opener_trim: Optional[bool] = None,
        closer_trim: Optional[bool] = None,
    ) -> "StringContent":
        instance = super().__new__(cls, value)
        instance.opener_trim = opener_trim
        instance.closer_trim = closer_trim
        return instance
    
    def __copy__(self) -> "StringContent":
        return StringContent(
            str(self), opener_trim=self.opener_trim, closer_trim=self.closer_trim
        )
    
    def __deepcopy__(self, memo: dict) -> "StringContent":
        result = StringContent(
            str(self), opener_trim=self.opener_trim, closer_trim=self.closer_trim
        )
        memo[id(self)] = result
        return result
    
    def __repr__(self) -> str:
        return (
            f"StringContent({str(self)!r}, "
            f"opener_trim={self.opener_trim}, closer_trim={self.closer_trim})"
        )


# Content item types that can appear in node content
ContentItem = Union[str, "StringContent", "NodeRef", "FileRef", "FlowNode"]


@dataclass
class FlowNode:
    """
    A node definition in the FLOW language.
    
    Attributes:
        id: Node identifier (e.g., "greeting", "_anon_123")
        params: Style, mutability, and strategy parameters
        slots: Named child slots defined with @slot_name |.|
        layer: Nesting depth for heading levels (0 = root)
        content: List of strings, refs, file refs, and nested nodes
        position: Source location for error reporting
    """
    id: str
    params: FlowParams = field(default_factory=FlowParams)
    slots: Dict[str, "FlowNode"] = field(default_factory=dict)
    layer: int = 0
    content: List[ContentItem] = field(default_factory=list)
    position: Optional[Position] = None
    
    @property
    def slot_count(self) -> int:
        """Count of slots defined in this node (for badge display)."""
        return len(self.slots)
    
    @property
    def slot_badge(self) -> str:
        """Display badge for slot count, or empty string if no slots."""
        count = self.slot_count
        if count == 0:
            return ""
        return f"[{count} slot{'s' if count != 1 else ''}]"
    
    def __repr__(self) -> str:
        return f"FlowNode(@{self.id}, layer={self.layer}, slots={list(self.slots.keys())}, content_len={len(self.content)})"


@dataclass
class ImportSelector:
    """
    A single import selector (node to import, optionally with rename).
    
    Attributes:
        original_name: The name in the source file
        local_name: The name in current file (same as original if no rename)
    """
    original_name: str
    local_name: str


@dataclass
class ImportNode:
    """
    An import statement (+./path/to/file.flow).
    
    Attributes:
        path: The file path to import from
        selectors: Specific nodes to import, or empty for all
        renames: Mapping of original names to local names (for renamed imports)
        position: Source location for error reporting
    """
    path: str
    selectors: List[str] = field(default_factory=list)
    renames: Dict[str, str] = field(default_factory=dict)
    position: Optional[Position] = None
    
    def __repr__(self) -> str:
        sel = f", selectors={self.selectors}" if self.selectors else ""
        ren = f", renames={self.renames}" if self.renames else ""
        return f"ImportNode(+{self.path}{sel}{ren})"


@dataclass
class Assignment:
    """
    An assignment statement ($parent.slot = $child).
    
    Attributes:
        target: The target path (e.g., "main.greeting")
        source: The source node id (e.g., "greeting")
        position: Source location for error reporting
    """
    target: str
    source: str
    position: Optional[Position] = None
    
    def __repr__(self) -> str:
        return f"Assignment(${self.target} = ${self.source})"


@dataclass
class FlowFile:
    """
    Root AST node representing a complete FLOW file.
    
    Attributes:
        imports: List of import statements
        nodes: Dict of node id to FlowNode
        assignments: List of assignment statements
        out_node: The @out entry point node (optional for libraries)
    """
    imports: List[ImportNode] = field(default_factory=list)
    nodes: Dict[str, FlowNode] = field(default_factory=dict)
    assignments: List[Assignment] = field(default_factory=list)
    out_node: Optional[FlowNode] = None
    
    def __repr__(self) -> str:
        return f"FlowFile(imports={len(self.imports)}, nodes={list(self.nodes.keys())}, assignments={len(self.assignments)}, has_out={self.out_node is not None})"


@dataclass
class ResolvedFlowFile:
    """
    Result of resolver stage - a fully validated and resolved AST.
    
    All references have been validated, imports merged, assignments applied,
    and dependency order computed for deterministic compilation.
    
    Attributes:
        nodes: All nodes (local + imported) after assignments applied
        out_node: The @out entry point with assignments applied (optional for libraries)
        dependency_order: Topological order of node IDs for compilation
        file_refs: List of ++path file references for validation
        source_path: Path to the source .flow file (for import resolution)
    """
    nodes: Dict[str, FlowNode] = field(default_factory=dict)
    out_node: Optional[FlowNode] = None
    dependency_order: List[str] = field(default_factory=list)
    file_refs: List[str] = field(default_factory=list)
    source_path: Optional[str] = None
    
    def __repr__(self) -> str:
        return (
            f"ResolvedFlowFile(nodes={list(self.nodes.keys())}, "
            f"has_out={self.out_node is not None}, "
            f"order={self.dependency_order[:3]}{'...' if len(self.dependency_order) > 3 else ''})"
        )


