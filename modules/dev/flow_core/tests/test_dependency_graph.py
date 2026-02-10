"""
Tests for Flow Language Dependency Graph (P1)

Comprehensive tests covering:
- DependencyGraph dataclass creation and methods
- Edge collection during resolution
- Graph export formats (DOT, JSON, Mermaid)
- Cross-file graph merging
- dependents() and dependencies() methods
"""

import pytest
import json
import tempfile
from pathlib import Path
import argparse

from flow_core.tokenizer import Tokenizer
from flow_core.parser import Parser, parse
from flow_core.resolver import Resolver, resolve, resolve_with_graph
from flow_core.dependency_graph import DependencyGraph, EdgeType
from flow_core.models import (
    FlowFile,
    FlowNode,
    NodeRef,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def tokenizer():
    """Provide a tokenizer instance."""
    return Tokenizer()


@pytest.fixture
def parser():
    """Provide a parser instance."""
    return Parser()


@pytest.fixture
def resolver():
    """Provide a resolver instance."""
    return Resolver()


def resolve_source_with_graph(source: str, base_path: Path = None) -> tuple:
    """Helper to tokenize, parse, and resolve with graph in one step."""
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(source)
    ast = parse(tokens)
    return resolve_with_graph(ast, base_path=base_path)


# =============================================================================
# DependencyGraph Dataclass Tests
# =============================================================================


class TestDependencyGraphDataclass:
    """Tests for the DependencyGraph dataclass itself."""
    
    def test_create_empty_graph(self):
        """Test creating an empty dependency graph."""
        graph = DependencyGraph.empty()
        
        assert len(graph.nodes) == 0
        assert len(graph.edges) == 0
        assert len(graph.files) == 0
        assert len(graph.file_refs) == 0
    
    def test_create_graph_with_data(self):
        """Test creating a dependency graph with data."""
        graph = DependencyGraph(
            nodes=frozenset(["a", "b", "c"]),
            edges=frozenset([("b", "a", EdgeType.BACKWARD_REF)]),
            files=frozenset([Path("/test/file.flow")]),
        )
        
        assert len(graph.nodes) == 3
        assert len(graph.edges) == 1
        assert len(graph.files) == 1
        # file_refs is computed from context_ref edges
        assert len(graph.file_refs) == 0
    
    def test_graph_is_frozen(self):
        """Test that DependencyGraph is immutable."""
        graph = DependencyGraph.empty()
        
        # frozenset is immutable, so we can't add to it
        with pytest.raises(AttributeError):
            graph.nodes.add("test")
    
    def test_dependents_method(self):
        """Test dependents() returns nodes that depend on given node."""
        graph = DependencyGraph(
            nodes=frozenset(["a", "b", "c"]),
            edges=frozenset([
                ("b", "a", EdgeType.BACKWARD_REF),
                ("c", "a", EdgeType.BACKWARD_REF),
            ]),
            files=frozenset(),
        )
        
        # Both b and c depend on a
        dependents = graph.dependents("a")
        assert dependents == {"b", "c"}
        
        # Nothing depends on b or c
        assert graph.dependents("b") == set()
        assert graph.dependents("c") == set()
    
    def test_dependencies_method(self):
        """Test dependencies() returns nodes that given node depends on."""
        graph = DependencyGraph(
            nodes=frozenset(["a", "b", "c"]),
            edges=frozenset([
                ("c", "a", EdgeType.BACKWARD_REF),
                ("c", "b", EdgeType.BACKWARD_REF),
            ]),
            files=frozenset(),
        )
        
        # c depends on both a and b
        deps = graph.dependencies("c")
        assert deps == {"a", "b"}
        
        # a and b don't depend on anything
        assert graph.dependencies("a") == set()
        assert graph.dependencies("b") == set()
    
    def test_edges_from_method(self):
        """Test edges_from() returns all edges from a node."""
        graph = DependencyGraph(
            nodes=frozenset(["a", "b", "c"]),
            edges=frozenset([
                ("c", "a", EdgeType.BACKWARD_REF),
                ("c", "b", EdgeType.FORWARD_REF),
            ]),
            files=frozenset(),
        )
        
        edges = graph.edges_from("c")
        assert len(edges) == 2
        assert ("c", "a", EdgeType.BACKWARD_REF) in edges
        assert ("c", "b", EdgeType.FORWARD_REF) in edges
    
    def test_edges_to_method(self):
        """Test edges_to() returns all edges to a node."""
        graph = DependencyGraph(
            nodes=frozenset(["a", "b", "c"]),
            edges=frozenset([
                ("b", "a", EdgeType.BACKWARD_REF),
                ("c", "a", EdgeType.FORWARD_REF),
            ]),
            files=frozenset(),
        )
        
        edges = graph.edges_to("a")
        assert len(edges) == 2


# =============================================================================
# Graph Building During Resolution Tests
# =============================================================================


class TestGraphBuilding:
    """Tests for graph building during resolution."""
    
    def test_simple_backward_ref_creates_edge(self):
        """Test that $ref creates a backward edge."""
        source = """
@greeting |<<<Hello>>>|.
@out |$greeting|.
"""
        resolved, graph = resolve_source_with_graph(source)
        
        assert "greeting" in graph.nodes
        assert "out" in graph.nodes
        assert ("out", "greeting", EdgeType.BACKWARD_REF) in graph.edges
    
    def test_forward_ref_creates_edge(self):
        """Test that ^ref creates a forward edge."""
        source = """
@preview |<<<Coming: >>>|^ending|.
@ending |<<<The End>>>|.
@out |$preview|.
"""
        resolved, graph = resolve_source_with_graph(source)
        
        assert ("preview", "ending", EdgeType.FORWARD_REF) in graph.edges
    
    def test_slot_ref_creates_edge(self):
        """Test that $node.slot creates a slot edge."""
        source = """
@parent |@slot |<<<Empty>>>|.|<<<Parent>>>|.

@user |$parent.slot|.
@out |$user|.
"""
        resolved, graph = resolve_source_with_graph(source)
        
        # User references parent.slot which creates a slot edge
        assert ("user", "parent", EdgeType.SLOT) in graph.edges
    
    def test_multiple_refs_create_multiple_edges(self):
        """Test that multiple references create multiple edges."""
        source = """
@a |<<<A>>>|.
@b |<<<B>>>|.
@c |$a|$b|.
@out |$c|.
"""
        resolved, graph = resolve_source_with_graph(source)
        
        assert ("c", "a", EdgeType.BACKWARD_REF) in graph.edges
        assert ("c", "b", EdgeType.BACKWARD_REF) in graph.edges
        assert ("out", "c", EdgeType.BACKWARD_REF) in graph.edges
    
    def test_file_refs_collected(self):
        """Test that ++path references are collected in graph."""
        source = """
@docs |<<<See: >>>|++./readme.md|.
@out |$docs|.
"""
        resolved, graph = resolve_source_with_graph(source)
        
        # File refs should be collected
        assert len(graph.file_refs) == 1
        assert any("readme.md" in str(p) for p in graph.file_refs)


# =============================================================================
# Graph Export Format Tests
# =============================================================================


class TestGraphExportFormats:
    """Tests for graph export formats."""
    
    def test_to_dot_basic(self):
        """Test DOT format export."""
        graph = DependencyGraph(
            nodes=frozenset(["a", "b"]),
            edges=frozenset([("b", "a", EdgeType.BACKWARD_REF)]),
            files=frozenset(),
        )
        
        dot = graph.to_dot()
        
        assert "digraph FlowDependencies" in dot
        assert '"a"' in dot
        assert '"b"' in dot
        assert '"b" -> "a"' in dot
        assert 'label="backward"' in dot
    
    def test_to_dot_escapes_special_chars(self):
        """Test DOT format escapes special characters in node names."""
        graph = DependencyGraph(
            nodes=frozenset(['node"with"quotes']),
            edges=frozenset(),
            files=frozenset(),
        )
        
        dot = graph.to_dot()
        
        # Quotes should be escaped
        assert '\\"' in dot
    
    def test_to_mermaid_basic(self):
        """Test Mermaid format export."""
        graph = DependencyGraph(
            nodes=frozenset(["a", "b"]),
            edges=frozenset([("b", "a", EdgeType.BACKWARD_REF)]),
            files=frozenset(),
        )
        
        mermaid = graph.to_mermaid()
        
        assert "flowchart TB" in mermaid
        assert '"a"' in mermaid
        assert '"b"' in mermaid
        assert "b -->|backward| a" in mermaid
    
    def test_to_mermaid_forward_ref_dotted(self):
        """Test Mermaid uses dotted arrow for forward refs."""
        graph = DependencyGraph(
            nodes=frozenset(["a", "b"]),
            edges=frozenset([("a", "b", EdgeType.FORWARD_REF)]),
            files=frozenset(),
        )
        
        mermaid = graph.to_mermaid()
        
        assert "-.->|forward|" in mermaid
    
    def test_to_json_basic(self):
        """Test JSON format export."""
        graph = DependencyGraph(
            nodes=frozenset(["a", "b"]),
            edges=frozenset([("b", "a", EdgeType.BACKWARD_REF)]),
            files=frozenset([Path("/test.flow")]),
        )
        
        json_str = graph.to_json()
        data = json.loads(json_str)
        
        assert "nodes" in data
        assert "edges" in data
        assert "files" in data
        assert "file_refs" in data
        
        assert "a" in data["nodes"]
        assert "b" in data["nodes"]
        
        assert len(data["edges"]) == 1
        edge = data["edges"][0]
        assert edge["from"] == "b"
        assert edge["to"] == "a"
        assert edge["type"] == EdgeType.BACKWARD_REF


# =============================================================================
# Graph Merging Tests (P1.5)
# =============================================================================


class TestGraphMerging:
    """Tests for cross-file graph merging."""
    
    def test_merge_empty_graphs(self):
        """Test merging empty graphs."""
        g1 = DependencyGraph.empty()
        g2 = DependencyGraph.empty()
        
        merged = DependencyGraph.merge(g1, g2)
        
        assert len(merged.nodes) == 0
        assert len(merged.edges) == 0
    
    def test_merge_disjoint_graphs(self):
        """Test merging graphs with no overlap."""
        g1 = DependencyGraph(
            nodes=frozenset(["a", "b"]),
            edges=frozenset([("b", "a", EdgeType.BACKWARD_REF)]),
            files=frozenset([Path("/file1.flow")]),
        )
        g2 = DependencyGraph(
            nodes=frozenset(["c", "d"]),
            edges=frozenset([("d", "c", EdgeType.BACKWARD_REF)]),
            files=frozenset([Path("/file2.flow")]),
        )
        
        merged = DependencyGraph.merge(g1, g2)
        
        assert merged.nodes == frozenset(["a", "b", "c", "d"])
        assert len(merged.edges) == 2
        assert len(merged.files) == 2
    
    def test_merge_overlapping_graphs(self):
        """Test merging graphs with shared nodes."""
        g1 = DependencyGraph(
            nodes=frozenset(["a", "b"]),
            edges=frozenset([("b", "a", EdgeType.BACKWARD_REF)]),
            files=frozenset(),
        )
        g2 = DependencyGraph(
            nodes=frozenset(["b", "c"]),
            edges=frozenset([("c", "b", EdgeType.BACKWARD_REF)]),
            files=frozenset(),
        )
        
        merged = DependencyGraph.merge(g1, g2)
        
        # Should have a, b, c (b appears in both)
        assert merged.nodes == frozenset(["a", "b", "c"])
        assert len(merged.edges) == 2
    
    def test_merge_multiple_graphs(self):
        """Test merging more than two graphs."""
        g1 = DependencyGraph(
            nodes=frozenset(["a"]),
            edges=frozenset(),
            files=frozenset(),
        )
        g2 = DependencyGraph(
            nodes=frozenset(["b"]),
            edges=frozenset(),
            files=frozenset(),
        )
        g3 = DependencyGraph(
            nodes=frozenset(["c"]),
            edges=frozenset(),
            files=frozenset(),
        )
        
        merged = DependencyGraph.merge(g1, g2, g3)
        
        assert merged.nodes == frozenset(["a", "b", "c"])


# =============================================================================
# Cross-File Graph Tests with Imports
# =============================================================================


class TestCrossFileGraph:
    """Tests for dependency graph with imports."""
    
    def test_import_adds_file_to_graph(self):
        """Test that importing a file adds it to graph.files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create imported file
            lib_path = Path(tmpdir) / "lib.flow"
            lib_path.write_text("@helper |<<<Help>>>|.\n")
            
            # Create main file - use relative import syntax
            main_source = "+./lib.flow |.\n@out |$helper|."
            
            tokenizer = Tokenizer()
            tokens = tokenizer.tokenize(main_source)
            ast = parse(tokens)
            
            resolved, graph = resolve_with_graph(
                ast,
                base_path=Path(tmpdir),
                source_path=str(Path(tmpdir) / "main.flow")
            )
            
            # Imported file should be in graph
            file_names = [f.name for f in graph.files]
            assert "lib.flow" in file_names

            # Explicit import edge should exist (file -> file)
            main_abs = str((Path(tmpdir) / "main.flow").resolve())
            lib_abs = str((Path(tmpdir) / "lib.flow").resolve())
            assert (main_abs, lib_abs, EdgeType.IMPORT) in graph.edges
    
    def test_imported_node_refs_create_edges(self):
        """Test that references to imported nodes create edges."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create imported file
            lib_path = Path(tmpdir) / "lib.flow"
            lib_path.write_text("@helper |<<<Help>>>|.\n")
            
            # Create main file - use relative import syntax
            main_source = "+./lib.flow |.\n@out |$helper|."
            
            tokenizer = Tokenizer()
            tokens = tokenizer.tokenize(main_source)
            ast = parse(tokens)
            
            resolved, graph = resolve_with_graph(
                ast,
                base_path=Path(tmpdir),
                source_path=str(Path(tmpdir) / "main.flow")
            )
            
            # Should have edge from out to helper
            assert ("out", "helper", EdgeType.BACKWARD_REF) in graph.edges


# =============================================================================
# Integration Tests
# =============================================================================


class TestDependencyGraphIntegration:
    """Integration tests for dependency graph with real Flow files."""
    
    def test_complex_graph_structure(self):
        """Test graph with multiple node types and references."""
        source = """
@intro |<<<Welcome>>>|.
@body |$intro|<<<Main content>>>|^conclusion|.
@conclusion |<<<The End>>>|.
@out |$body|.
"""
        resolved, graph = resolve_source_with_graph(source)
        
        # Verify all nodes present
        assert graph.nodes == frozenset(["intro", "body", "conclusion", "out"])
        
        # Verify edges
        assert ("body", "intro", EdgeType.BACKWARD_REF) in graph.edges
        assert ("body", "conclusion", EdgeType.FORWARD_REF) in graph.edges
        assert ("out", "body", EdgeType.BACKWARD_REF) in graph.edges
    
    def test_graph_with_nested_nodes(self):
        """Test that nested node refs are tracked correctly."""
        source = """
@parent |@child |<<<Nested>>>|.|<<<Parent content>>>|.

@user |$parent|.
@out |$user|.
"""
        resolved, graph = resolve_source_with_graph(source)
        
        # user references parent, out references user
        assert ("user", "parent", EdgeType.BACKWARD_REF) in graph.edges
        assert ("out", "user", EdgeType.BACKWARD_REF) in graph.edges


# =============================================================================
# Edge Type Tests
# =============================================================================


class TestEdgeTypes:
    """Tests for different edge types."""
    
    def test_edge_type_values(self):
        """Test that edge types have correct string values."""
        assert EdgeType.BACKWARD_REF == "backward"
        assert EdgeType.FORWARD_REF == "forward"
        assert EdgeType.IMPORT == "import"
        assert EdgeType.SLOT == "slot"


# =============================================================================
# P1 Gap Tests: Stress & Edge Cases
# =============================================================================


class TestLargeGraphStress:
    """
    P1 Gap Test (Priority 2): Large graph stress tests with 50+ nodes.
    
    Verifies graph building performance and correctness at scale.
    """
    
    def test_large_graph_50_nodes(self):
        """Test graph with 50 nodes and chain dependencies."""
        # Build a chain: @node1 -> @node2 -> ... -> @node50 -> @out
        nodes = []
        for i in range(1, 51):
            nodes.append(f"@node{i} |<<<Content {i}>>>|.")
        
        # Create chain references: each node references the previous
        refs_source = "\n".join([
            f"@chain{i} |$node{i}|." for i in range(1, 51)
        ])
        
        # Final @out references last chain node
        source = "\n".join(nodes) + "\n" + refs_source + "\n@out |$chain50|."
        
        resolved, graph = resolve_source_with_graph(source)
        
        # Should have 50 nodes + 50 chain nodes + 1 out = 101 nodes
        assert len(graph.nodes) == 101
        
        # Should have 50 edges from chain nodes to nodes + 1 from out
        assert len(graph.edges) == 51
    
    def test_large_graph_all_connected(self):
        """Test graph where many nodes reference a single hub node."""
        # Create a hub node
        source = "@hub |<<<Hub>>>|.\n"
        
        # Create 50 nodes all referencing the hub
        for i in range(1, 51):
            source += f"@spoke{i} |$hub|<<<Spoke {i}>>>|.\n"
        
        # @out references last spoke
        source += "@out |$spoke50|."
        
        resolved, graph = resolve_source_with_graph(source)
        
        # Should have hub + 50 spokes + out = 52 nodes
        assert len(graph.nodes) == 52
        
        # 50 edges from spokes to hub + 1 edge from out to spoke50
        assert len(graph.edges) == 51
        
        # Verify dependents of hub includes all spokes
        hub_dependents = graph.dependents("hub")
        assert len(hub_dependents) == 50


class TestCircularRefEdgeCases:
    """
    P1 Gap Test (Priority 3): Circular reference edge cases.
    
    Verifies circular dependencies are properly detected.
    """
    
    def test_circular_ref_detected_forward_backward(self):
        """Test that circular ref with forward+backward refs is detected."""
        # a uses forward ref to b, b uses backward ref to a -> cycle
        source = """
@a |^b|.
@b |$a|.
@out |$b|.
"""
        from flow_core.errors import CircularDependencyError
        
        with pytest.raises(CircularDependencyError):
            resolve_source_with_graph(source)
    
    def test_three_node_cycle_detection(self):
        """Test detection of 3-node cycle using forward refs."""
        # Using forward refs: a->b, b->c, c->a creates cycle
        source = """
@a |^b|.
@b |^c|.
@c |^a|.
@out |$c|.
"""
        from flow_core.errors import CircularDependencyError
        
        with pytest.raises(CircularDependencyError):
            resolve_source_with_graph(source)


class TestTransitiveImportChain:
    """
    P1 Gap Test (Priority 5): Transitive import chains (3+ files).
    
    Verifies graph correctly merges nodes from deep import chains.
    """
    
    def test_three_file_import_chain(self):
        """Test graph merging with A imports B imports C.

        Uses forward refs (^) in intermediate files since imports are processed
        after the local symbol table is built.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create file C (deepest) - standalone library
            c_path = Path(tmpdir) / "c.flow"
            c_path.write_text("@deep |<<<Deep content>>>|.\n")
            
            # Create file B (imports C) - library that uses deep
            # Must use forward ref (^deep) since import is processed after local nodes
            b_path = Path(tmpdir) / "b.flow"
            b_path.write_text("+./c.flow |.\n@middle |^deep|<<<Middle>>>|.\n")
            
            # Create file A (main, imports B) - uses middle
            # Can use backward ref ($middle) since imports are processed first in parent
            a_source = "+./b.flow |.\n@top |$middle|<<<Top>>>|.\n@out |$top|."
            
            tokenizer = Tokenizer()
            tokens = tokenizer.tokenize(a_source)
            ast = parse(tokens)
            
            resolved, graph = resolve_with_graph(
                ast,
                base_path=Path(tmpdir),
                source_path=str(Path(tmpdir) / "a.flow")
            )
            
            # Graph should include all involved files (including transitive)
            file_names = {f.name for f in graph.files}
            assert "a.flow" in file_names
            assert "b.flow" in file_names
            assert "c.flow" in file_names

            # Import edges should include both hops
            a_abs = str((Path(tmpdir) / "a.flow").resolve())
            b_abs = str((Path(tmpdir) / "b.flow").resolve())
            c_abs = str((Path(tmpdir) / "c.flow").resolve())
            assert (a_abs, b_abs, EdgeType.IMPORT) in graph.edges
            assert (b_abs, c_abs, EdgeType.IMPORT) in graph.edges

            # All nodes should be present (including transitively imported)
            assert "deep" in graph.nodes
            assert "middle" in graph.nodes
            assert "top" in graph.nodes
            assert "out" in graph.nodes

            # Edges should show the dependency chain
            assert ("middle", "deep", EdgeType.FORWARD_REF) in graph.edges
            assert ("top", "middle", EdgeType.BACKWARD_REF) in graph.edges
            assert ("out", "top", EdgeType.BACKWARD_REF) in graph.edges

    def test_mermaid_sanitizes_file_path_nodes(self):
        """Mermaid export should remain valid even when node IDs are file paths."""
        graph = DependencyGraph(
            nodes=frozenset(["/tmp/a.flow", "@out", "out"]),
            edges=frozenset([
                ("/tmp/a.flow", "/tmp/b.flow", EdgeType.IMPORT),
                ("out", "/tmp/readme.md", EdgeType.CONTEXT_REF),
            ]),
            files=frozenset(),
        )
        mermaid = graph.to_mermaid()
        assert "flowchart TB" in mermaid
        assert "import" in mermaid
        assert "context_ref" in mermaid
    
    def test_parallel_imports_no_conflict(self):
        """Test that parallel imports with unique nodes work correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create file B with unique node
            b_path = Path(tmpdir) / "b.flow"
            b_path.write_text("@b_node |<<<B content>>>|.\n")
            
            # Create file C with different unique node
            c_path = Path(tmpdir) / "c.flow"
            c_path.write_text("@c_node |<<<C content>>>|.\n")
            
            # Create file A (imports B and C)
            a_source = "+./b.flow |.\n+./c.flow |.\n@out |$b_node|$c_node|."
            
            tokenizer = Tokenizer()
            tokens = tokenizer.tokenize(a_source)
            ast = parse(tokens)
            
            resolved, graph = resolve_with_graph(
                ast,
                base_path=Path(tmpdir),
                source_path=str(Path(tmpdir) / "a.flow")
            )
            
            # All nodes should be present
            assert "b_node" in graph.nodes
            assert "c_node" in graph.nodes
            assert "out" in graph.nodes
            
            # Edges should show both dependencies
            assert ("out", "b_node", EdgeType.BACKWARD_REF) in graph.edges
            assert ("out", "c_node", EdgeType.BACKWARD_REF) in graph.edges
