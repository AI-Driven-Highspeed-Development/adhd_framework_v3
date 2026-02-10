"""
Flow Core Error Classes

Defines the exception hierarchy for the Flow language compiler.
"""

from exceptions_core import ADHDError


class FlowError(ADHDError):
    """
    Base error for all Flow language compiler errors.
    
    All Flow-related exceptions should inherit from this class
    to allow for unified error handling.
    """
    
    def __init__(self, message: str, line: int = 0, column: int = 0) -> None:
        self.line = line
        self.column = column
        location = f" at line {line}, column {column}" if line > 0 else ""
        super().__init__(f"{message}{location}")


class TokenizerError(FlowError):
    """
    Tokenizer-specific errors.
    
    Raised when the tokenizer encounters invalid syntax or
    unexpected characters in the source.
    """
    pass


class UnclosedStringError(TokenizerError):
    """
    String block not properly closed.
    
    Raised when a <<< or << string block opener is not matched
    by a corresponding >>> or >> closer before end of input.
    """
    
    def __init__(self, opener: str, line: int, column: int) -> None:
        self.opener = opener
        super().__init__(
            f"Unclosed string block starting with '{opener}'",
            line=line,
            column=column
        )


class InvalidTokenError(TokenizerError):
    """
    Invalid or unexpected token encountered.
    
    Raised when the tokenizer cannot recognize a valid token
    at the current position.
    """
    
    def __init__(self, char: str, line: int, column: int) -> None:
        self.char = char
        super().__init__(
            f"Invalid character '{char}'",
            line=line,
            column=column
        )


# =============================================================================
# Parser Errors
# =============================================================================


class ParserError(FlowError):
    """
    Parser-specific errors.
    
    Raised when the parser encounters invalid syntax or
    unexpected token sequences.
    """
    pass


class UnexpectedTokenError(ParserError):
    """
    Unexpected token encountered during parsing.
    
    Raised when the parser encounters a token that doesn't match
    the expected grammar at the current position.
    """
    
    def __init__(
        self,
        got: str,
        expected: list[str],
        line: int,
        column: int,
        context: str = ""
    ) -> None:
        self.got = got
        self.expected = expected
        self.context = context
        
        expected_str = " or ".join(f"'{e}'" for e in expected)
        ctx_str = f" {context}" if context else ""
        super().__init__(
            f"Unexpected '{got}', expected {expected_str}{ctx_str}",
            line=line,
            column=column
        )


class DuplicateNodeError(ParserError):
    """
    Duplicate node definition.
    
    Raised when a node with the same ID is defined more than once.
    Includes positions of both definitions for debugging.
    """
    
    def __init__(
        self,
        node_id: str,
        first_line: int,
        first_column: int,
        second_line: int,
        second_column: int,
        first_file: str = "",
        second_file: str = ""
    ) -> None:
        self.node_id = node_id
        self.first_line = first_line
        self.first_column = first_column
        self.second_line = second_line
        self.second_column = second_column
        self.first_file = first_file
        self.second_file = second_file
        
        # Build location strings
        first_loc = f"line {first_line}, col {first_column}"
        if first_file:
            first_loc = f"{first_file}:{first_loc}"
        second_loc = f"line {second_line}, col {second_column}"
        if second_file:
            second_loc = f"{second_file}:{second_loc}"
            
        super().__init__(
            f"Duplicate node definition '@{node_id}' "
            f"(first at {first_loc}; second at {second_loc})",
            line=second_line,
            column=second_column
        )


# =============================================================================
# Resolver Errors
# =============================================================================


class ResolverError(FlowError):
    """
    Resolver-specific errors.
    
    Raised during semantic analysis and reference resolution.
    """
    pass


class UndefinedNodeError(ResolverError):
    """
    Reference to undefined node.
    
    Raised when $id or ^id references a node that doesn't exist
    or violates reference constraints (e.g., $ref must be above).
    """
    
    def __init__(
        self,
        ref_id: str,
        line: int,
        column: int,
        is_forward: bool = False,
        constraint_msg: str = ""
    ) -> None:
        self.ref_id = ref_id
        self.is_forward = is_forward
        prefix = "^" if is_forward else "$"
        constraint = f" ({constraint_msg})" if constraint_msg else ""
        super().__init__(
            f"Undefined node reference '{prefix}{ref_id}'{constraint}",
            line=line,
            column=column
        )


class UndefinedSlotError(ResolverError):
    """
    Reference to undefined slot.
    
    Raised when $node.slot references a slot that doesn't exist
    on the target node.
    """
    
    def __init__(
        self,
        node_id: str,
        slot_name: str,
        line: int,
        column: int
    ) -> None:
        self.node_id = node_id
        self.slot_name = slot_name
        super().__init__(
            f"Undefined slot '{slot_name}' on node '@{node_id}'",
            line=line,
            column=column
        )


class CircularDependencyError(ResolverError):
    """
    Circular reference detected between nodes.
    
    Raised when nodes form a dependency cycle that cannot be resolved.
    Includes the full chain for debugging.
    """
    
    def __init__(self, chain: list[str], line: int = 0, column: int = 0) -> None:
        self.chain = chain
        chain_str = " → ".join(f"@{node}" for node in chain)
        super().__init__(
            f"Circular dependency detected: {chain_str}",
            line=line,
            column=column
        )


class ImportFileNotFoundError(ResolverError):
    """
    Import file does not exist.
    
    Raised when +./path/to/file.flow references a file that
    cannot be found on disk.
    """
    
    def __init__(
        self,
        import_path: str,
        resolved_path: str,
        line: int,
        column: int
    ) -> None:
        self.import_path = import_path
        self.resolved_path = resolved_path
        super().__init__(
            f"Import file not found: '{import_path}' (resolved to '{resolved_path}')",
            line=line,
            column=column
        )


class CircularImportError(ResolverError):
    """
    Circular import detected between files.
    
    Raised when file A imports file B which imports file A
    (directly or transitively).
    """
    
    def __init__(self, chain: list[str], line: int = 0, column: int = 0) -> None:
        self.chain = chain
        chain_str = " → ".join(chain)
        super().__init__(
            f"Circular import detected: {chain_str}",
            line=line,
            column=column
        )


# =============================================================================
# Compiler Errors
# =============================================================================


class CompilerError(FlowError):
    """
    Compiler-specific errors.
    
    Raised during the compilation phase when transforming
    resolved AST to Markdown output.
    """
    pass


class MissingOutNodeError(CompilerError):
    """
    Entry point file lacks @out node.
    
    Raised when attempting to compile a FlowFile that is
    not a library (expects an entry point) but has no @out node.
    """
    
    def __init__(self, file_path: str = "") -> None:
        self.file_path = file_path
        location = f" in '{file_path}'" if file_path else ""
        super().__init__(
            f"Missing @out entry point node{location}. "
            "Either define @out or mark the file as a library.",
            line=0,
            column=0
        )



