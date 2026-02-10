"""
Flow Language Tokenizer

Converts Flow language source code into a stream of tokens.
Handles all Flow syntax elements including string blocks with
asymmetric pairing, node definitions, references, and operators.
"""

from typing import List, Optional

from logger_util import Logger
from .models import Token, TokenType
from .errors import (
    TokenizerError,
    UnclosedStringError,
    InvalidTokenError,
)


class Tokenizer:
    """
    Tokenizer for the Flow language.
    
    Converts source code into a list of Token objects, tracking
    line and column numbers for error reporting.
    
    Flow Syntax Elements:
        - Comments: # at line start
        - Imports: + at line start (+./path/to/file.flow)
        - Node definitions: @name
        - Node references: $name
        - Forward references: ^name
        - File references: ++path
        - Pipe operator: |
        - Node terminator: |.
        - Assignment: =
        - String blocks: <<<...>>> (trim) or <<...>> (preserve)
    """
    
    def __init__(self, logger: Optional[Logger] = None) -> None:
        """
        Initialize the tokenizer.
        
        Args:
            logger: Optional logger instance.
        """
        self.logger = logger or Logger(name="FlowTokenizer")
        self._source: str = ""
        self._pos: int = 0
        self._line: int = 1
        self._column: int = 1
        self._tokens: List[Token] = []
        self._line_start: bool = True  # Track if we're at line start
    
    def tokenize(self, source: str) -> List[Token]:
        """
        Tokenize Flow language source code.
        
        Args:
            source: The source code string to tokenize.
            
        Returns:
            List of Token objects.
            
        Raises:
            TokenizerError: On tokenization errors.
            UnclosedStringError: If a string block is not closed.
        """
        if source.startswith('\ufeff'):
            source = source[1:]
        self._source = source
        self._pos = 0
        self._line = 1
        self._column = 1
        self._tokens = []
        self._line_start = True
        
        self.logger.debug(f"Tokenizing {len(source)} characters")
        
        while not self._at_end():
            self._scan_token()
        
        # Add EOF token
        self._add_token_at(TokenType.EOF, "", self._line, self._column)
        
        self.logger.debug(f"Produced {len(self._tokens)} tokens")
        return self._tokens
    
    def _at_end(self) -> bool:
        """Check if we've reached the end of source."""
        return self._pos >= len(self._source)
    
    def _peek(self, offset: int = 0) -> str:
        """Look at character at current position + offset without consuming."""
        pos = self._pos + offset
        if pos >= len(self._source):
            return "\0"
        return self._source[pos]
    
    def _peek_string(self, length: int) -> str:
        """Look at the next 'length' characters without consuming."""
        return self._source[self._pos : self._pos + length]
    
    def _advance(self) -> str:
        """Consume and return the current character."""
        char = self._source[self._pos]
        self._pos += 1
        
        if char == "\n":
            self._line += 1
            self._column = 1
            self._line_start = True
        else:
            self._column += 1
            if not char.isspace():
                self._line_start = False
        
        return char
    
    def _advance_n(self, n: int) -> str:
        """Consume and return the next n characters."""
        chars = []
        for _ in range(n):
            if not self._at_end():
                chars.append(self._advance())
        return "".join(chars)
    
    def _skip_whitespace(self) -> None:
        """Skip whitespace characters (except newlines which are tracked)."""
        while not self._at_end():
            char = self._peek()
            if char in " \t\r":
                self._advance()
            elif char == "\n":
                self._advance()
            else:
                break
    
    def _scan_token(self) -> None:
        """Scan and produce the next token."""
        # Skip leading whitespace
        self._skip_whitespace()
        
        if self._at_end():
            return
        
        # Record position before scanning
        start_line = self._line
        start_column = self._column
        char = self._peek()
        
        # Check for multi-character operators first
        two_chars = self._peek_string(2)
        three_chars = self._peek_string(3)
        
        # String block openers (check 3-char before 2-char)
        if three_chars == "<<<":
            self._scan_string_block(trim=True, start_line=start_line, start_column=start_column)
            return
        
        if two_chars == "<<":
            self._scan_string_block(trim=False, start_line=start_line, start_column=start_column)
            return
        
        # File reference: ++path
        if two_chars == "++":
            self._advance_n(2)
            self._scan_file_ref(start_line, start_column)
            return
        
        # Node terminator: |.
        if two_chars == "|.":
            self._advance_n(2)
            self._add_token_at(TokenType.DOT_END, "|.", start_line, start_column)
            return
        
        # Escaped pipe: \| (should be treated as literal content, but only after string blocks)
        # This will be handled in context - for now we tokenize \ separately
        
        # Single character tokens
        char = self._advance()
        
        if char == "#" and self._was_line_start(start_column):
            # Comment - consume rest of line
            self._scan_comment(start_line, start_column)
            
        elif char == "+" and self._was_line_start(start_column):
            # Import
            self._scan_import(start_line, start_column)
            
        elif char == "@":
            # Node definition
            self._scan_node_def(start_line, start_column)
            
        elif char == "$":
            # Node reference
            self._scan_node_ref(start_line, start_column)
            
        elif char == "^":
            # Forward reference
            self._scan_forward_ref(start_line, start_column)
            
        elif char == "|":
            # Pipe operator
            self._add_token_at(TokenType.PIPE, "|", start_line, start_column)
            
        elif char == "=":
            # Assignment
            self._add_token_at(TokenType.ASSIGN, "=", start_line, start_column)
            
        elif char == "\\":
            # Escape character - check what follows
            if self._peek() == "|":
                # Escaped pipe - treat as identifier for now
                self._advance()  # consume the |
                self._add_token_at(TokenType.IDENTIFIER, "\\|", start_line, start_column)
            else:
                # Lone backslash - could be part of content
                self._add_token_at(TokenType.IDENTIFIER, "\\", start_line, start_column)
            
        elif self._is_identifier_start(char):
            # Identifier
            self._scan_identifier(char, start_line, start_column)
        
        elif char == ">":
            # Stray > character - provide helpful error message
            raise TokenizerError(
                "Unexpected '>' - did you mean '>>' or '>>>' to close a string block?",
                line=start_line,
                column=start_column
            )
            
        else:
            # Unknown character - could be part of content in certain contexts
            # For now, raise an error
            raise InvalidTokenError(char, start_line, start_column)
    
    def _was_line_start(self, column: int) -> bool:
        """Check if the given column was at the start of a line."""
        return column == 1
    
    def _add_token_at(
        self, token_type: TokenType, value: str, line: int, column: int,
        *, closer_trim: Optional[bool] = None,
    ) -> None:
        """Add a token with explicit position."""
        token = Token(type=token_type, value=value, line=line, column=column,
                      closer_trim=closer_trim)
        self._tokens.append(token)
        self.logger.debug(f"Token: {token}")
    
    def _is_identifier_start(self, char: str) -> bool:
        """Check if character can start an identifier."""
        return char.isalpha() or char == "_"
    
    def _is_identifier_char(self, char: str) -> bool:
        """Check if character can be part of an identifier."""
        return char.isalnum() or char == "_" or char == "."
    
    def _scan_comment(self, start_line: int, start_column: int) -> None:
        """Scan a comment (# at line start)."""
        chars = []
        while not self._at_end() and self._peek() != "\n":
            chars.append(self._advance())
        
        # Include the # in the value
        self._add_token_at(TokenType.COMMENT, "#" + "".join(chars), start_line, start_column)
    
    def _scan_import(self, start_line: int, start_column: int) -> None:
        """Scan an import directive (+ at line start)."""
        # Skip any whitespace after +
        while not self._at_end() and self._peek() in " \t":
            self._advance()
        
        # Consume the path
        chars = []
        while not self._at_end() and self._peek() not in " \t\n\r|":
            chars.append(self._advance())
        path = "".join(chars)
        
        # Validate that a path was provided
        if not path:
            raise TokenizerError(
                "Expected path after '+'", line=start_line, column=start_column
            )
        
        self._add_token_at(TokenType.IMPORT, path, start_line, start_column)
    
    def _scan_identifier_name(self, prefix_char: str, start_line: int, start_column: int) -> str:
        """
        Scan an identifier name after a prefix character (@, $, ^).
        
        Args:
            prefix_char: The prefix that triggered this scan (for error messages).
            start_line: Line where scanning started.
            start_column: Column where scanning started.
            
        Returns:
            The scanned identifier name.
            
        Raises:
            TokenizerError: If no valid identifier follows the prefix.
        """
        # First character MUST be a valid identifier start (letter or underscore)
        if self._at_end() or not self._is_identifier_start(self._peek()):
            char = self._peek() if not self._at_end() else "EOF"
            raise TokenizerError(
                f"Expected identifier after '{prefix_char}', got '{char}'",
                line=start_line,
                column=start_column,
            )
        
        chars = [self._advance()]  # Consume first character (already validated)
        while not self._at_end() and self._is_identifier_char(self._peek()):
            chars.append(self._advance())
        return "".join(chars)
    
    def _scan_node_def(self, start_line: int, start_column: int) -> None:
        """Scan a node definition (@name)."""
        name = self._scan_identifier_name("@", start_line, start_column)
        self._add_token_at(TokenType.NODE_DEF, name, start_line, start_column)
    
    def _scan_node_ref(self, start_line: int, start_column: int) -> None:
        """Scan a node reference ($name or $name.slot)."""
        name = self._scan_identifier_name("$", start_line, start_column)
        self._add_token_at(TokenType.NODE_REF, name, start_line, start_column)
    
    def _scan_forward_ref(self, start_line: int, start_column: int) -> None:
        """Scan a forward reference (^name)."""
        name = self._scan_identifier_name("^", start_line, start_column)
        self._add_token_at(TokenType.FORWARD_REF, name, start_line, start_column)
    
    def _scan_file_ref(self, start_line: int, start_column: int) -> None:
        """Scan a file reference (++path)."""
        # Skip any whitespace after ++
        while not self._at_end() and self._peek() in " \t":
            self._advance()
        
        # Consume the path
        chars = []
        while not self._at_end() and self._peek() not in " \t\n\r|":
            chars.append(self._advance())
        path = "".join(chars)
        
        if not path:
            raise TokenizerError(
                "Expected path after '++'", line=start_line, column=start_column
            )
        
        self._add_token_at(TokenType.FILE_REF, path, start_line, start_column)
    
    def _scan_identifier(
        self, first_char: str, start_line: int, start_column: int
    ) -> None:
        """Scan an identifier."""
        chars = [first_char]
        while not self._at_end() and self._is_identifier_char(self._peek()):
            chars.append(self._advance())
        
        self._add_token_at(TokenType.IDENTIFIER, "".join(chars), start_line, start_column)
    
    def _scan_string_block(
        self, trim: bool, start_line: int, start_column: int
    ) -> None:
        r"""
        Scan a string block.
        
        String blocks can have asymmetric pairing:
        - <<< can close with >>> OR >>
        - << can close with >> OR >>>
        
        The opener controls LEADING whitespace, the closer controls TRAILING:
        - <<< (trim opener) + >>> (trim closer) = trim both ends
        - << (preserve opener) + >> (preserve closer) = preserve both ends
        - <<< (trim opener) + >> (preserve closer) = trim leading, preserve trailing
        - << (preserve opener) + >>> (trim closer) = preserve leading, trim trailing
        
        Escape handling:
        - >>>\| or >>\| means "include literal >>>| or >>| in content"
        - The escape ONLY applies if there's more content after the |
        - If \| is at EOF or end of meaningful content, >>> or >> closes the string
        
        Args:
            trim: True if opened with <<<, False if opened with <<
            start_line: Line where the block started
            start_column: Column where the block started
        """
        # Track opener mode for leading whitespace
        opener_is_trim = trim
        
        # Consume the opener
        opener = "<<<" if opener_is_trim else "<<"
        self._advance_n(len(opener))
        
        content_chars: list[str] = []
        content_start_line = self._line
        content_start_column = self._column
        
        while not self._at_end():
            # Check for closers (>>> first, then >>)
            three_chars = self._peek_string(3)
            two_chars = self._peek_string(2)
            
            if three_chars == ">>>":
                # Check if this is an escaped sequence: >>>\|
                # Only treat as escape if there's more content after the |
                five_chars = self._peek_string(5)

                if five_chars == r">>>\|":
                    # Check if there's actual content after the | (not just EOF)
                    # Position after >>>\| would be pos+5
                    char_after = self._peek(5)  # Character after >>>\|
                    if char_after != "\0":  # Not at EOF
                        # Escaped: consume >>> and \, add >>>| to content
                        self._advance_n(3)  # consume >>>
                        self._advance()     # consume \
                        self._advance()     # consume |
                        content_chars.append(">>>|")
                        continue
                
                # Not escaped (or escape at EOF) - this is a real closer
                # >>> is a trim closer
                closer_is_trim = True
                self._advance_n(3)
                
                # Token type based on opener (indicates author's primary intent)
                token_type = TokenType.STRING_TRIM if opener_is_trim else TokenType.STRING_PRESERVE
                content = "".join(content_chars)
                final_content = self._process_string_content(content, opener_is_trim, closer_is_trim)
                self._add_token_at(token_type, final_content, start_line, start_column,
                                   closer_trim=closer_is_trim)
                return
            
            if two_chars == ">>":
                # Check if this is an escaped sequence: >>\|
                # Only treat as escape if there's more content after the |
                four_chars = self._peek_string(4)
                
                if four_chars == r">>\|":
                    # Check if there's actual content after the | (not just EOF)
                    char_after = self._peek(4)  # Character after >>\|
                    if char_after != "\0":  # Not at EOF
                        # Escaped: consume >> and \, add >>| to content
                        self._advance_n(2)  # consume >>
                        self._advance()     # consume \
                        self._advance()     # consume |
                        content_chars.append(">>|")
                        continue
                
                # Not escaped (or escape at EOF) - this is a real closer
                # >> is a preserve closer
                closer_is_trim = False
                self._advance_n(2)
                
                # Token type based on opener (indicates author's primary intent)
                token_type = TokenType.STRING_TRIM if opener_is_trim else TokenType.STRING_PRESERVE
                content = "".join(content_chars)
                final_content = self._process_string_content(content, opener_is_trim, closer_is_trim)
                self._add_token_at(token_type, final_content, start_line, start_column,
                                   closer_trim=closer_is_trim)
                return
            
            # Consume character as part of content
            content_chars.append(self._advance())
        
        # Reached end without finding closer
        raise UnclosedStringError(opener, start_line, start_column)
    
    def _process_string_content(self, content: str, trim_leading: bool, trim_trailing: bool) -> str:
        """
        Process string block content with asymmetric trimming.
        
        Args:
            content: The raw content between delimiters.
            trim_leading: If True, trim leading whitespace (opener was <<<).
            trim_trailing: If True, trim trailing whitespace (closer was >>>).
            
        Returns:
            Processed content string.
        """
        result = content
        
        if trim_leading:
            # Remove leading whitespace (newlines, spaces, tabs)
            result = result.lstrip()
        
        if trim_trailing:
            # Remove trailing whitespace (newlines, spaces, tabs)
            result = result.rstrip()
        
        return result
