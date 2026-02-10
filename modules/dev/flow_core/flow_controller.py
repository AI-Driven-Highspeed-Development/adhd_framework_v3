"""
Flow Controller - Main orchestration for Flow language compilation.

This module coordinates the full compilation pipeline:
1. Tokenization: Source → Tokens
2. Parsing: Tokens → AST (FlowFile)
3. Resolution: AST → Resolved AST (ResolvedFlowFile)
4. Compilation: Resolved AST → Markdown

Usage:
    >>> from flow_core.flow_controller import FlowController
    >>> controller = FlowController()
    >>> markdown = controller.compile_source(source_code)
    >>> # Or from file:
    >>> markdown = controller.compile_file(Path("document.flow"))
"""

from pathlib import Path
from typing import List, Optional, Set

from logger_util import Logger
from .models import Token, FlowFile, ResolvedFlowFile
from .tokenizer import Tokenizer
from .parser import Parser
from .resolver import Resolver
from .compiler import Compiler


class FlowController:
    """
    Main controller for Flow language compilation.
    
    Coordinates the full pipeline: tokenization → parsing → resolution → compilation.
    Provides both granular stage access and convenience methods for full compilation.
    
    Stages:
        1. tokenize(): Source string → List[Token]
        2. parse(): List[Token] → FlowFile (AST)
        3. resolve(): FlowFile → ResolvedFlowFile
        4. compile(): ResolvedFlowFile → Markdown string
    
    Convenience methods:
        - compile_source(): Source string → Markdown (runs all stages)
        - compile_file(): File path → Markdown (reads file, runs all stages)
    """
    
    def __init__(self, logger: Optional[Logger] = None) -> None:
        """
        Initialize the Flow controller.
        
        Args:
            logger: Optional logger instance. Creates one if not provided.
        """
        self.logger = logger or Logger(name="FlowController")
        self._tokenizer = Tokenizer(logger=self.logger)
        self._parser = Parser(logger=self.logger)
        self._resolver = Resolver(logger=self.logger)
        self._compiler = Compiler(logger=self.logger)
    
    # =========================================================================
    # Stage 1: Tokenization
    # =========================================================================
    
    def tokenize(self, source: str) -> List[Token]:
        """
        Tokenize Flow language source code.
        
        Args:
            source: The Flow language source code string.
            
        Returns:
            List of tokens extracted from the source.
            
        Raises:
            TokenizerError: If tokenization fails.
        """
        self.logger.debug("Starting tokenization")
        tokens = self._tokenizer.tokenize(source)
        self.logger.debug(f"Tokenization complete: {len(tokens)} tokens")
        return tokens
    
    def tokenize_file(self, file_path: Path) -> List[Token]:
        """
        Tokenize a Flow language source file.
        
        Args:
            file_path: Path to the .flow file.
            
        Returns:
            List of tokens extracted from the file.
            
        Raises:
            FileNotFoundError: If the file doesn't exist.
            TokenizerError: If tokenization fails.
        """
        self.logger.info(f"Tokenizing file: {file_path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"Flow file not found: {file_path}")
        
        source = file_path.read_text(encoding="utf-8")
        return self.tokenize(source)
    
    # =========================================================================
    # Stage 2: Parsing
    # =========================================================================
    
    def parse(self, tokens: List[Token]) -> FlowFile:
        """
        Parse tokens into a FlowFile AST.
        
        Args:
            tokens: List of tokens from tokenization.
            
        Returns:
            FlowFile AST.
            
        Raises:
            ParserError: On syntax errors.
            DuplicateNodeError: On duplicate node definitions.
        """
        self.logger.debug("Starting parsing")
        flow_file = self._parser.parse(tokens)
        self.logger.debug(f"Parsing complete: {len(flow_file.nodes)} nodes")
        return flow_file
    
    def parse_source(self, source: str) -> FlowFile:
        """
        Tokenize and parse source code in one step.
        
        Args:
            source: The Flow language source code string.
            
        Returns:
            FlowFile AST.
        """
        tokens = self.tokenize(source)
        return self.parse(tokens)
    
    # =========================================================================
    # Stage 3: Resolution
    # =========================================================================
    
    def resolve(
        self,
        flow_file: FlowFile,
        base_path: Optional[Path] = None,
        source_path: Optional[str] = None
    ) -> ResolvedFlowFile:
        """
        Resolve a FlowFile AST.
        
        Validates references, processes imports, applies assignments,
        and computes dependency order.
        
        Args:
            flow_file: The parsed FlowFile AST.
            base_path: Base directory for import resolution.
            source_path: Path to source file (for error messages).
            
        Returns:
            ResolvedFlowFile with all references resolved.
            
        Raises:
            UndefinedNodeError: Reference to non-existent node.
            CircularDependencyError: Cycle in node references.
            ImportFileNotFoundError: Import file not found.
        """
        self.logger.debug("Starting resolution")
        resolved = self._resolver.resolve(flow_file, base_path, source_path)
        self.logger.debug(f"Resolution complete: {len(resolved.nodes)} nodes")
        return resolved
    
    def get_last_resolved_files(self) -> Set[Path]:
        """Return the set of all .flow files that participated in the last resolve.

        This includes the entry .flow file and every transitively imported .flow
        file.  Useful for computing transitive hashes so that changes in shared
        fragments trigger recompilation of dependants.

        Returns:
            A **copy** of the resolver's graph-files set, or an empty set if
            no resolve has been performed yet.
        """
        return set(self._resolver._graph_files)
    
    # =========================================================================
    # Stage 4: Compilation
    # =========================================================================
    
    def compile(
        self,
        resolved: ResolvedFlowFile,
        require_out: bool = True
    ) -> str:
        """
        Compile a resolved FlowFile to Markdown.
        
        Args:
            resolved: The resolved FlowFile AST.
            require_out: If True, raise error when @out is missing.
            
        Returns:
            Compiled Markdown string.
            
        Raises:
            MissingOutNodeError: If require_out=True and no @out.
        """
        self.logger.debug("Starting compilation")
        markdown = self._compiler.compile(resolved, require_out)
        self.logger.debug(f"Compilation complete: {len(markdown)} chars")
        return markdown
    
    # =========================================================================
    # Convenience Methods (Full Pipeline)
    # =========================================================================
    
    def compile_source(
        self,
        source: str,
        base_path: Optional[Path] = None,
        require_out: bool = True
    ) -> str:
        """
        Compile Flow source code to Markdown (full pipeline).
        
        Runs all stages: tokenize → parse → resolve → compile.
        
        Args:
            source: The Flow language source code string.
            base_path: Base directory for import resolution.
            require_out: If True, raise error when @out is missing.
            
        Returns:
            Compiled Markdown string.
            
        Raises:
            TokenizerError, ParserError, ResolverError, CompilerError
        
        Example:
            >>> controller = FlowController()
            >>> source = '''
            ... @greeting |<<<Hello, World!>>>|.
            ... @out |$greeting|.
            ... '''
            >>> print(controller.compile_source(source))
            Hello, World!
        """
        self.logger.info("Compiling source (full pipeline)")
        
        # Stage 1: Tokenize
        tokens = self.tokenize(source)
        
        # Stage 2: Parse
        flow_file = self.parse(tokens)
        
        # Stage 3: Resolve
        resolved = self.resolve(flow_file, base_path)
        
        # Stage 4: Compile
        return self.compile(resolved, require_out)
    
    def compile_file(
        self,
        file_path: Path,
        require_out: bool = True
    ) -> str:
        """
        Compile a Flow file to Markdown (full pipeline).
        
        Reads the file and runs all compilation stages.
        Uses the file's directory as base_path for import resolution.
        
        Args:
            file_path: Path to the .flow file.
            require_out: If True, raise error when @out is missing.
            
        Returns:
            Compiled Markdown string.
            
        Raises:
            FileNotFoundError: If the file doesn't exist.
            TokenizerError, ParserError, ResolverError, CompilerError
        
        Example:
            >>> controller = FlowController()
            >>> markdown = controller.compile_file(Path("docs/intro.flow"))
        """
        self.logger.info(f"Compiling file: {file_path}")
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Flow file not found: {file_path}")
        
        # Read source
        source = file_path.read_text(encoding="utf-8")
        
        # Use file's directory as base path for imports
        base_path = file_path.parent.resolve()
        
        # Stage 1: Tokenize
        tokens = self.tokenize(source)
        
        # Stage 2: Parse
        flow_file = self.parse(tokens)
        
        # Stage 3: Resolve (with file context)
        resolved = self.resolve(
            flow_file,
            base_path=base_path,
            source_path=str(file_path)
        )
        
        # Stage 4: Compile
        return self.compile(resolved, require_out)


# =============================================================================
# Module-Level Convenience Functions
# =============================================================================


def compile_flow(source: str, logger: Optional[Logger] = None) -> str:
    """
    Compile Flow source code to Markdown.
    
    This is the simplest entry point for Flow compilation.
    
    Args:
        source: The Flow language source code string.
        logger: Optional logger instance.
        
    Returns:
        Compiled Markdown string.
    
    Example:
        >>> from flow_core import compile_flow
        >>> source = '''
        ... @greeting |<<<Hello!>>>|.
        ... @out |$greeting|.
        ... '''
        >>> print(compile_flow(source))
        Hello!
    """
    controller = FlowController(logger=logger)
    return controller.compile_source(source)


def compile_flow_file(file_path: Path, logger: Optional[Logger] = None) -> str:
    """
    Compile a Flow file to Markdown.
    
    Args:
        file_path: Path to the .flow file.
        logger: Optional logger instance.
        
    Returns:
        Compiled Markdown string.
    """
    controller = FlowController(logger=logger)
    return controller.compile_file(file_path)
