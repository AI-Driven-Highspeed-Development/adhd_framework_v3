"""
Flow Language Parser

Transforms a token stream into a typed Abstract Syntax Tree (AST).
Uses recursive descent parsing to build FlowFile, FlowNode, ImportNode,
and Assignment structures from the tokenized input.
"""

from typing import List, Optional, Dict, Tuple

from logger_util import Logger
from .models import (
    Token,
    TokenType,
    Position,
    FlowParams,
    FlowStyle,
    FlowLLMStrategy,
    FlowNode,
    NodeRef,
    FileRef,
    ImportNode,
    Assignment,
    FlowFile,
    ContentItem,
    StringContent,
)
from .errors import (
    ParserError,
    UnexpectedTokenError,
    DuplicateNodeError,
)


class Parser:
    """
    Recursive descent parser for the Flow language.
    
    Transforms a list of tokens into a FlowFile AST containing:
    - Import statements
    - Node definitions with parameters, slots, and content
    - Assignment statements
    - Reference to the @out entry point
    """
    
    def __init__(self, logger: Optional[Logger] = None) -> None:
        """
        Initialize the parser.
        
        Args:
            logger: Optional logger instance for debugging.
        """
        self.logger = logger or Logger(name="FlowParser")
        self._tokens: List[Token] = []
        self._pos: int = 0
        self._nodes: Dict[str, FlowNode] = {}
        self._node_positions: Dict[str, Position] = {}  # Track first definition positions
        self._imports: List[ImportNode] = []
        self._assignments: List[Assignment] = []
        self._anon_counter: int = 0  # For generating anonymous node IDs
    
    def parse(self, tokens: List[Token]) -> FlowFile:
        """
        Parse a token stream into a FlowFile AST.
        
        Args:
            tokens: List of tokens from the tokenizer.
            
        Returns:
            FlowFile AST representing the parsed FLOW document.
            
        Raises:
            ParserError: On syntax errors.
            DuplicateNodeError: When a node ID is defined twice.
            UnexpectedTokenError: On unexpected token sequences.
        """
        self._tokens = tokens
        self._pos = 0
        self._nodes = {}
        self._node_positions = {}
        self._imports = []
        self._assignments = []
        self._anon_counter = 0
        
        self.logger.debug(f"Parsing {len(tokens)} tokens")
        
        while not self._at_end():
            self._parse_top_level()
        
        # Build FlowFile
        out_node = self._nodes.get("out")
        
        flow_file = FlowFile(
            imports=self._imports,
            nodes=self._nodes,
            assignments=self._assignments,
            out_node=out_node,
        )
        
        self.logger.debug(f"Parsed: {flow_file}")
        return flow_file
    
    # =========================================================================
    # Token Navigation
    # =========================================================================
    
    def _at_end(self) -> bool:
        """Check if we've reached EOF."""
        return self._pos >= len(self._tokens) or self._peek().type == TokenType.EOF
    
    def _peek(self, offset: int = 0) -> Token:
        """Look at token at current position + offset without consuming."""
        pos = self._pos + offset
        if pos >= len(self._tokens):
            return self._tokens[-1]  # Return EOF token
        return self._tokens[pos]
    
    def _advance(self) -> Token:
        """Consume and return the current token."""
        token = self._tokens[self._pos]
        if token.type != TokenType.EOF:
            self._pos += 1
        return token
    
    def _check(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        if self._at_end():
            return TokenType.EOF in token_types
        return self._peek().type in token_types
    
    def _match(self, *token_types: TokenType) -> Optional[Token]:
        """If current token matches any type, consume and return it."""
        if self._check(*token_types):
            return self._advance()
        return None
    
    def _expect(self, token_type: TokenType, context: str = "") -> Token:
        """Consume a token of the expected type, or raise an error."""
        token = self._peek()
        if token.type != token_type:
            raise UnexpectedTokenError(
                got=token.value or token.type.name,
                expected=[token_type.name],
                line=token.line,
                column=token.column,
                context=context,
            )
        return self._advance()
    
    def _position(self, token: Token) -> Position:
        """Create a Position from a token."""
        return Position(line=token.line, column=token.column)
    
    # =========================================================================
    # Top-Level Parsing
    # =========================================================================
    
    def _parse_top_level(self) -> None:
        """Parse a top-level statement (import, node def, assignment, or comment)."""
        token = self._peek()
        
        if token.type == TokenType.COMMENT:
            # Skip comments
            self._advance()
            
        elif token.type == TokenType.IMPORT:
            # Import statement
            import_node = self._parse_import()
            self._imports.append(import_node)
            
        elif token.type == TokenType.NODE_DEF:
            # Node definition
            node = self._parse_node_def(parent_layer=-1)
            self._register_node(node)
            
        elif token.type == TokenType.NODE_REF:
            # Could be an assignment: $a.slot = $b
            assignment = self._parse_assignment()
            self._assignments.append(assignment)
            
        elif token.type == TokenType.EOF:
            # End of file
            return
            
        else:
            raise UnexpectedTokenError(
                got=token.value or token.type.name,
                expected=["COMMENT", "IMPORT", "NODE_DEF", "NODE_REF", "EOF"],
                line=token.line,
                column=token.column,
                context="at top level",
            )
    
    def _register_node(self, node: FlowNode) -> None:
        """Register a node, checking for duplicates."""
        if node.id in self._nodes:
            first_pos = self._node_positions[node.id]
            raise DuplicateNodeError(
                node_id=node.id,
                first_line=first_pos.line,
                first_column=first_pos.column,
                second_line=node.position.line if node.position else 0,
                second_column=node.position.column if node.position else 0,
            )
        self._nodes[node.id] = node
        if node.position:
            self._node_positions[node.id] = node.position
    
    # =========================================================================
    # Import Parsing
    # =========================================================================
    
    def _parse_import(self) -> ImportNode:
        """
        Parse an import statement.
        
        Syntax:
            +./path/to/file.flow |.                     # Import all
            +./path/to/file.flow | $node1 | $node2 |.   # Import specific
            +./path/to/file.flow | @alias|. = $original |.  # Import with rename
        """
        import_token = self._advance()  # Consume IMPORT token
        path = import_token.value
        position = self._position(import_token)
        
        selectors: List[str] = []
        renames: Dict[str, str] = {}
        
        # Check for pipe (optional selectors/renames follow)
        while self._match(TokenType.PIPE):
            # Check what follows the pipe
            if self._check(TokenType.DOT_END):
                # Just |. - end of import, but we matched PIPE, not DOT_END
                # Actually DOT_END is |. as a single token, so check for it
                break
            
            if self._check(TokenType.NODE_REF):
                # $node_name - selector
                ref_token = self._advance()
                selectors.append(ref_token.value)
                
            elif self._check(TokenType.NODE_DEF):
                # @alias |. = $original - rename
                alias_token = self._advance()
                alias_name = alias_token.value
                
                # Expect |.
                self._expect(TokenType.DOT_END, "after rename alias")
                
                # Expect =
                self._expect(TokenType.ASSIGN, "in rename")
                
                # Expect $original
                orig_token = self._expect(TokenType.NODE_REF, "after = in rename")
                original_name = orig_token.value
                
                renames[original_name] = alias_name
                selectors.append(original_name)
        
        # Consume final |.
        self._expect(TokenType.DOT_END, "at end of import")
        
        return ImportNode(
            path=path,
            selectors=selectors,
            renames=renames,
            position=position,
        )
    
    # =========================================================================
    # Node Definition Parsing
    # =========================================================================
    
    def _parse_node_def(self, parent_layer: int) -> FlowNode:
        """
        Parse a node definition.
        
        Syntax:
            @id |param=value|<<<content>>>|@slot|.|.
        
        Args:
            parent_layer: The layer of the parent node (-1 for top-level).
            
        Returns:
            The parsed FlowNode.
        """
        node_token = self._advance()  # Consume NODE_DEF token
        
        # Handle anonymous node (@_)
        if node_token.value == "_":
            node_id = self._generate_anon_id(node_token)
        else:
            node_id = node_token.value
        
        position = self._position(node_token)
        layer = parent_layer + 1
        
        params = FlowParams()
        slots: Dict[str, FlowNode] = {}
        content: List[ContentItem] = []
        
        # Parse pipe-separated sections until |.
        while self._match(TokenType.PIPE):
            if self._check(TokenType.DOT_END):
                # Empty section before |.
                break
            
            # Determine what kind of section this is
            token = self._peek()
            
            if token.type == TokenType.NODE_DEF:
                # Nested slot definition: @slot_name |...|.
                slot_node = self._parse_slot_def(layer)
                slots[slot_node.id] = slot_node
                content.append(slot_node)
                
            elif token.type == TokenType.IDENTIFIER:
                # Parameter: key=value
                param_name, param_value = self._parse_param()
                self._apply_param(params, param_name, param_value)
                
            elif token.type in (TokenType.STRING_TRIM, TokenType.STRING_PRESERVE):
                # String content — wrap in StringContent to carry trim metadata
                string_token = self._advance()
                opener_trim = (string_token.type == TokenType.STRING_TRIM)
                sc = StringContent(
                    string_token.value,
                    opener_trim=opener_trim,
                    closer_trim=string_token.closer_trim,
                )
                content.append(sc)
                
            elif token.type == TokenType.NODE_REF:
                # Node reference: $id
                ref_token = self._advance()
                ref = NodeRef(
                    id=ref_token.value,
                    is_forward=False,
                    position=self._position(ref_token),
                )
                content.append(ref)
                
            elif token.type == TokenType.FORWARD_REF:
                # Forward reference: ^id
                ref_token = self._advance()
                ref = NodeRef(
                    id=ref_token.value,
                    is_forward=True,
                    position=self._position(ref_token),
                )
                content.append(ref)
                
            elif token.type == TokenType.FILE_REF:
                # File reference: ++path
                file_token = self._advance()
                file_ref = FileRef(
                    path=file_token.value,
                    position=self._position(file_token),
                )
                content.append(file_ref)
                
            else:
                raise UnexpectedTokenError(
                    got=token.value or token.type.name,
                    expected=["NODE_DEF", "IDENTIFIER", "STRING", "NODE_REF", "FORWARD_REF", "FILE_REF"],
                    line=token.line,
                    column=token.column,
                    context=f"in node @{node_id}",
                )
        
        # Consume final |.
        self._expect(TokenType.DOT_END, f"at end of node @{node_id}")
        
        return FlowNode(
            id=node_id,
            params=params,
            slots=slots,
            layer=layer,
            content=content,
            position=position,
        )
    
    def _parse_slot_def(self, parent_layer: int) -> FlowNode:
        """
        Parse a slot definition (nested node within a node).
        
        Syntax:
            @slot_name |...|.
        
        The slot inherits layer = parent_layer + 1.
        """
        return self._parse_node_def(parent_layer)
    
    def _generate_anon_id(self, token: Token) -> str:
        """Generate a deterministic anonymous node ID based on position."""
        self._anon_counter += 1
        return f"_anon_{token.line}_{token.column}_{self._anon_counter}"
    
    # =========================================================================
    # Parameter Parsing
    # =========================================================================
    
    def _parse_param(self) -> Tuple[str, str]:
        """
        Parse a parameter: key=value
        
        Returns:
            Tuple of (param_name, param_value).
        """
        # Get the identifier (may have dots: style.title)
        name_token = self._advance()  # Already checked it's IDENTIFIER
        param_name = name_token.value
        
        # Expect =
        self._expect(TokenType.ASSIGN, f"after parameter name '{param_name}'")
        
        # Get value (can be string, identifier, etc.)
        value_token = self._peek()
        
        if value_token.type in (TokenType.STRING_TRIM, TokenType.STRING_PRESERVE):
            value_token = self._advance()
            param_value = value_token.value
        elif value_token.type == TokenType.IDENTIFIER:
            value_token = self._advance()
            param_value = value_token.value
        else:
            raise UnexpectedTokenError(
                got=value_token.value or value_token.type.name,
                expected=["STRING", "IDENTIFIER"],
                line=value_token.line,
                column=value_token.column,
                context=f"for parameter value of '{param_name}'",
            )
        
        return param_name, param_value
    
    def _apply_param(self, params: FlowParams, name: str, value: str) -> None:
        """Apply a parsed parameter to the FlowParams object."""
        # Handle dotted parameter names
        parts = name.split(".")
        
        if parts[0] == "style":
            if params.style is None:
                params.style = FlowStyle()
            if len(parts) > 1:
                style_param = parts[1]
                if style_param == "title":
                    params.style.title = value
                elif style_param == "divider":
                    params.style.divider = value.lower() in ("true", "1", "yes")
                elif style_param == "list":
                    # Validate list type
                    valid_types = {"bullet", "numbered", "task", "task-done"}
                    if value not in valid_types:
                        self.logger.warning(f"Invalid list type '{value}', valid: {valid_types}")
                    params.style.list_type = value
                elif style_param == "wrap":
                    # Validate wrap type
                    valid_wraps = {"xml", "codeblock", "blockquote", "details"}
                    if value.lower() not in valid_wraps:
                        self.logger.warning(f"Invalid wrap type '{value}', valid: {valid_wraps}")
                    params.style.wrap = value
                elif style_param == "tag":
                    params.style.tag = value
                elif style_param == "summary":
                    params.style.summary = value
                elif style_param == "level":
                    # Handle level=N (absolute) or level=+N (relative offset)
                    self._parse_style_level(params.style, value)
                else:
                    self.logger.debug(f"Unknown style parameter: {style_param}={value}")
                
        elif parts[0] == "llm_strategy":
            if params.llm_strategy is None:
                params.llm_strategy = FlowLLMStrategy()
            if len(parts) > 1 and parts[1] == "instruction":
                params.llm_strategy.instruction = value
                
        elif name == "mutable":
            params.mutable = value.lower() in ("true", "1", "yes")
            
        elif name == "remutate":
            params.remutate = value.lower() in ("true", "1", "yes")
        
        # Ignore unknown parameters (could warn via logger)
        else:
            self.logger.debug(f"Unknown parameter: {name}={value}")
    
    def _parse_style_level(self, style: FlowStyle, value: str) -> None:
        """
        Parse level parameter value into style.level or style.level_offset.
        
        Supports two syntaxes:
        - level=N   → Absolute heading level (1-6)
        - level=+N  → Relative offset added to layer-based level
        
        Args:
            style: The FlowStyle object to update.
            value: The parameter value (e.g., "3" or "+2").
        """
        value = value.strip()
        
        if value.startswith("+"):
            # Relative offset: level=+N
            try:
                offset = int(value[1:])
                style.level_offset = offset
            except ValueError:
                self.logger.warning(f"Invalid level offset value: '{value}', expected +N where N is integer")
        else:
            # Absolute level: level=N
            try:
                level = int(value)
                if level < 1 or level > 6:
                    self.logger.warning(f"Level {level} out of range, will be clamped to 1-6")
                style.level = level
            except ValueError:
                self.logger.warning(f"Invalid level value: '{value}', expected integer 1-6 or +N offset")
    
    # =========================================================================
    # Assignment Parsing
    # =========================================================================
    
    def _parse_assignment(self) -> Assignment:
        """
        Parse an assignment statement.
        
        Syntax:
            $parent.slot = $child
        """
        # Get target: $parent.slot
        target_token = self._advance()  # Already checked it's NODE_REF
        target = target_token.value
        position = self._position(target_token)
        
        # Expect =
        self._expect(TokenType.ASSIGN, "in assignment")
        
        # Get source: $child
        source_token = self._expect(TokenType.NODE_REF, "after = in assignment")
        source = source_token.value
        
        return Assignment(
            target=target,
            source=source,
            position=position,
        )


# =============================================================================
# Module-Level Parse Function
# =============================================================================


def parse(tokens: List[Token], logger: Optional[Logger] = None) -> FlowFile:
    """
    Parse a token stream into a FlowFile AST.
    
    This is the main entry point for parsing FLOW tokens.
    
    Args:
        tokens: List of tokens from the tokenizer.
        logger: Optional logger instance.
        
    Returns:
        FlowFile AST representing the parsed document.
        
    Raises:
        ParserError: On syntax errors.
        DuplicateNodeError: On duplicate node definitions.
        UnexpectedTokenError: On unexpected tokens.
    
    Example:
        >>> from flow_core.tokenizer import tokenize
        >>> from flow_core.parser import parse
        >>> tokens = tokenize("@greeting |<<<Hello!>>>|.\n@out |$greeting|.")
        >>> ast = parse(tokens)
        >>> print(ast.nodes.keys())
        dict_keys(['greeting', 'out'])
    """
    parser = Parser(logger=logger)
    return parser.parse(tokens)
