"""
Tests for Flow CLI Commands (P1.0, P1.3, P1.4)

Tests covering:
- tokenize command
- parse command
- resolve command
- compile command
- graph command (DOT, JSON, Mermaid formats)
- validate command
"""

import pytest
import json
from pathlib import Path
from io import StringIO
from unittest.mock import patch
import argparse

from flow_core.flow_cli import (
    tokenize_command,
    parse_command,
    resolve_command,
    compile_command,
    graph_command,
    validate_command,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def sample_flow_file(tmp_path) -> Path:
    """Create a sample .flow file for testing."""
    flow_file = tmp_path / "test.flow"
    flow_file.write_text("""
@greeting |<<<Hello, World!>>>|.
@out |$greeting|.
""")
    return flow_file


@pytest.fixture
def invalid_flow_file(tmp_path) -> Path:
    """Create an invalid .flow file for testing."""
    flow_file = tmp_path / "invalid.flow"
    flow_file.write_text("""
@out |$undefined_node|.
""")
    return flow_file


@pytest.fixture
def complex_flow_file(tmp_path) -> Path:
    """Create a complex .flow file with multiple reference types."""
    flow_file = tmp_path / "complex.flow"
    flow_file.write_text("""
@intro |<<<Welcome>>>|.
@body |$intro|<<<Main content>>>|^conclusion|.
@conclusion |<<<The End>>>|.
@out |$body|.
""")
    return flow_file


# =============================================================================
# Tokenize Command Tests
# =============================================================================


class TestTokenizeCommand:
    """Tests for the tokenize CLI command."""
    
    def test_tokenize_valid_file(self, sample_flow_file):
        """Test tokenizing a valid Flow file."""
        exit_code = tokenize_command(argparse.Namespace(file=str(sample_flow_file), verbose=False))
        assert exit_code == 0
    
    def test_tokenize_nonexistent_file(self, tmp_path):
        """Test tokenizing a nonexistent file."""
        nonexistent = tmp_path / "nonexistent.flow"
        exit_code = tokenize_command(argparse.Namespace(file=str(nonexistent), verbose=False))
        assert exit_code == 1
    
    def test_tokenize_with_verbose(self, sample_flow_file):
        """Test tokenizing with verbose flag."""
        exit_code = tokenize_command(argparse.Namespace(file=str(sample_flow_file), verbose=True))
        assert exit_code == 0


# =============================================================================
# Parse Command Tests
# =============================================================================


class TestParseCommand:
    """Tests for the parse CLI command."""
    
    def test_parse_valid_file(self, sample_flow_file):
        """Test parsing a valid Flow file."""
        exit_code = parse_command(argparse.Namespace(file=str(sample_flow_file), verbose=False))
        assert exit_code == 0
    
    def test_parse_with_verbose(self, sample_flow_file):
        """Test parsing with verbose flag."""
        exit_code = parse_command(argparse.Namespace(file=str(sample_flow_file), verbose=True))
        assert exit_code == 0
    
    def test_parse_nonexistent_file(self, tmp_path):
        """Test parsing a nonexistent file."""
        nonexistent = tmp_path / "nonexistent.flow"
        exit_code = parse_command(argparse.Namespace(file=str(nonexistent), verbose=False))
        assert exit_code == 1


# =============================================================================
# Resolve Command Tests
# =============================================================================


class TestResolveCommand:
    """Tests for the resolve CLI command."""
    
    def test_resolve_valid_file(self, sample_flow_file):
        """Test resolving a valid Flow file."""
        exit_code = resolve_command(argparse.Namespace(file=str(sample_flow_file), verbose=False))
        assert exit_code == 0
    
    def test_resolve_invalid_file(self, invalid_flow_file):
        """Test resolving an invalid Flow file."""
        exit_code = resolve_command(argparse.Namespace(file=str(invalid_flow_file), verbose=False))
        assert exit_code == 1
    
    def test_resolve_with_verbose(self, sample_flow_file):
        """Test resolving with verbose flag."""
        exit_code = resolve_command(argparse.Namespace(file=str(sample_flow_file), verbose=True))
        assert exit_code == 0


# =============================================================================
# Compile Command Tests
# =============================================================================


class TestCompileCommand:
    """Tests for the compile CLI command."""
    
    def test_compile_valid_file(self, sample_flow_file, capsys):
        """Test compiling a valid Flow file."""
        exit_code = compile_command(argparse.Namespace(file=str(sample_flow_file), output=None))
        assert exit_code == 0
        
        captured = capsys.readouterr()
        assert "Hello, World!" in captured.out
    
    def test_compile_to_output_file(self, sample_flow_file, tmp_path):
        """Test compiling with output file."""
        output_file = tmp_path / "output.md"
        exit_code = compile_command(argparse.Namespace(file=str(sample_flow_file), output=str(output_file)))
        
        assert exit_code == 0
        assert output_file.exists()
        content = output_file.read_text()
        assert "Hello, World!" in content
    
    def test_compile_nonexistent_file(self, tmp_path):
        """Test compiling a nonexistent file."""
        nonexistent = tmp_path / "nonexistent.flow"
        exit_code = compile_command(argparse.Namespace(file=str(nonexistent), output=None))
        assert exit_code == 1


# =============================================================================
# Graph Command Tests
# =============================================================================


class TestGraphCommand:
    """Tests for the graph CLI command."""
    
    def test_graph_mermaid_format(self, sample_flow_file, capsys):
        """Test graph command with Mermaid format (default)."""
        exit_code = graph_command(argparse.Namespace(file=str(sample_flow_file), format="mermaid"))
        
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "flowchart TB" in captured.out
        assert "greeting" in captured.out
        assert "out" in captured.out
    
    def test_graph_mermaid_explicit(self, sample_flow_file, capsys):
        """Test graph command with explicit Mermaid format."""
        exit_code = graph_command(argparse.Namespace(file=str(sample_flow_file), format="mermaid"))
        
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "flowchart TB" in captured.out
    
    def test_graph_dot_format(self, sample_flow_file, capsys):
        """Test graph command with DOT format."""
        exit_code = graph_command(argparse.Namespace(file=str(sample_flow_file), format="dot"))
        
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "digraph FlowDependencies" in captured.out
        assert "greeting" in captured.out
        assert "out" in captured.out
    
    def test_graph_json_format(self, sample_flow_file, capsys):
        """Test graph command with JSON format."""
        exit_code = graph_command(argparse.Namespace(file=str(sample_flow_file), format="json"))
        
        assert exit_code == 0
        captured = capsys.readouterr()
        
        # Should be valid JSON
        data = json.loads(captured.out)
        assert "nodes" in data
        assert "edges" in data
        assert "greeting" in data["nodes"]
        assert "out" in data["nodes"]
    
    def test_graph_complex_file(self, complex_flow_file, capsys):
        """Test graph command with complex file containing multiple ref types."""
        exit_code = graph_command(argparse.Namespace(file=str(complex_flow_file), format="json"))
        
        assert exit_code == 0
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        
        # Should have all nodes
        assert {"intro", "body", "conclusion", "out"}.issubset(set(data["nodes"]))
        
        # Should have edges for different ref types
        edge_types = [e["type"] for e in data["edges"]]
        assert "backward" in edge_types  # $intro
        assert "forward" in edge_types   # ^conclusion
    
    def test_graph_invalid_format(self, sample_flow_file):
        """Test graph command with invalid format."""
        exit_code = graph_command(argparse.Namespace(file=str(sample_flow_file), format="invalid"))
        assert exit_code == 1


# =============================================================================
# Validate Command Tests
# =============================================================================


class TestValidateCommand:
    """Tests for the validate CLI command."""
    
    def test_validate_valid_file(self, sample_flow_file):
        """Test validating a valid Flow file."""
        exit_code = validate_command(argparse.Namespace(file=str(sample_flow_file)))
        assert exit_code == 0
    
    def test_validate_invalid_file(self, invalid_flow_file):
        """Test validating an invalid Flow file."""
        exit_code = validate_command(argparse.Namespace(file=str(invalid_flow_file)))
        assert exit_code == 1
    
    def test_validate_nonexistent_file(self, tmp_path):
        """Test validating a nonexistent file."""
        nonexistent = tmp_path / "nonexistent.flow"
        exit_code = validate_command(argparse.Namespace(file=str(nonexistent)))
        assert exit_code == 1
    
    def test_validate_multi_error_file(self, tmp_path):
        """
        P1 Gap Test: Validate command reports errors for multi-error file.
        
        Tests that validation detects and reports errors. Currently the resolver
        stops at the first error in resolution phase, but the validate command
        infrastructure supports collecting multiple errors across stages.
        """
        # Create a file with multiple semantic issues:
        # - node1 references two undefined nodes
        # - node2 references node1 via invalid backward ref (node1 is below)
        multi_error_file = tmp_path / "multi_error.flow"
        multi_error_file.write_text("""
    @node2 |$node1|$undefined_c|.
    @node1 |$undefined_a|$undefined_b|.
    @out |$node2|.
""")

        # Capture JSON output to verify multiple errors are reported
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            exit_code = validate_command(argparse.Namespace(file=str(multi_error_file)))
            output = fake_out.getvalue()

        data = json.loads(output)
        assert data["success"] is False
        assert "errors" in data
        # Should report more than one semantic error
        assert len(data["errors"]) >= 2
        
        # Should fail validation with exit code 1
        assert exit_code == 1
    
    def test_validate_empty_file(self, tmp_path):
        """
        P1 Gap Test: Validate command handles empty file gracefully.
        
        Edge case: Empty file should be valid (library mode, no @out required).
        """
        empty_file = tmp_path / "empty.flow"
        empty_file.write_text("")

        exit_code = validate_command(argparse.Namespace(file=str(empty_file)))
        
        # Empty file is valid (library mode)
        assert exit_code == 0
