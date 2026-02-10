"""
Spec Tests for Tiered Visibility Implementation
================================================

Test plan from HyperSan covering:
- Priority 1 (BLOCKER): Model properties (slot_count, slot_badge)
- Priority 2 (BLOCKER): Tier filtering (slot edge visibility, badges)
- Priority 3 (WARNING): CLI commands (graph, inspect, debug)

Run with: pytest playground/test_tiered_visibility_spec.py -v
"""

import argparse
import json
from pathlib import Path

import pytest

from flow_core.models import (
    FlowNode, FlowParams,
)
from flow_core.dependency_graph import DependencyGraph, EdgeType, Tier
from flow_core.tokenizer import Tokenizer
from flow_core.parser import Parser
from flow_core.resolver import resolve_with_graph
from flow_core.flow_cli import (
    graph_command, inspect_command, debug_command
)
from logger_util import Logger


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def flow_file_with_slots(tmp_path) -> Path:
    """Create a Flow file with slots for tier testing.
    
    Container has 3 inline slots (header, body, footer).
    Assignment mutates the header slot.
    """
    flow_file = tmp_path / "with_slots.flow"
    # Note: Slots are defined INLINE within @container, not referenced internally
    flow_file.write_text("""
@container |@header |<<<Default Header>>>|.| @body |<<<Default Body>>>|.| @footer |<<<Default Footer>>>|.|<<<Container.>>>|.

@custom_header |<<<Custom Header>>>|.

$container.header = $custom_header

@out |$container|.
""")
    return flow_file


@pytest.fixture
def logger():
    """Create a logger for testing."""
    return Logger(name="TestTieredVisibility")


# =============================================================================
# Priority 1 (BLOCKER) - Model Properties
# =============================================================================

class TestSlotCount:
    """Tests for FlowNode.slot_count property."""
    
    def test_slot_count_zero_for_no_slots(self):
        """Node with no slots should have slot_count of 0."""
        node = FlowNode(id="simple", params=FlowParams())
        assert node.slot_count == 0
    
    def test_slot_count_returns_correct_count(self):
        """Node with slots should return correct count."""
        node = FlowNode(
            id="container",
            params=FlowParams(),
            slots={
                "header": FlowNode(id="container.header"),
                "body": FlowNode(id="container.body"),
                "footer": FlowNode(id="container.footer"),
            }
        )
        assert node.slot_count == 3


class TestSlotBadge:
    """Tests for FlowNode.slot_badge property."""
    
    def test_slot_badge_empty_when_no_slots(self):
        """Node with no slots should have empty badge string."""
        node = FlowNode(id="simple", params=FlowParams())
        assert node.slot_badge == ""
    
    def test_slot_badge_singular_form(self):
        """Node with 1 slot should use singular 'slot'."""
        node = FlowNode(
            id="container",
            params=FlowParams(),
            slots={"only_slot": FlowNode(id="container.only_slot")}
        )
        assert node.slot_badge == "[1 slot]"
    
    def test_slot_badge_plural_form(self):
        """Node with multiple slots should use plural 'slots'."""
        node = FlowNode(
            id="container",
            params=FlowParams(),
            slots={
                "header": FlowNode(id="container.header"),
                "body": FlowNode(id="container.body"),
                "footer": FlowNode(id="container.footer"),
            }
        )
        assert node.slot_badge == "[3 slots]"


# =============================================================================
# Priority 2 (BLOCKER) - Tier Filtering
# =============================================================================

class TestTierFiltering:
    """Tests for DependencyGraph tier-based filtering."""
    
    @pytest.fixture
    def graph_with_slot_edges(self):
        """Create a graph with both regular and slot edges."""
        return DependencyGraph(
            nodes=frozenset(["container", "container.header", "helper", "out"]),
            edges=frozenset([
                ("out", "container", EdgeType.BACKWARD_REF),
                ("container", "helper", EdgeType.BACKWARD_REF),
                ("container", "container.header", EdgeType.SLOT),  # Slot edge
            ]),
            files=frozenset([Path("/test/file.flow")]),
        )
    
    def test_tier_0_hides_slot_edges(self, graph_with_slot_edges):
        """Tier 0 (structural) should hide slot edges in exports."""
        # Export as JSON at tier 0
        json_output = graph_with_slot_edges.to_json(tier=Tier.STRUCTURAL)
        data = json.loads(json_output)
        
        # Slot edges should be filtered out
        edge_types = [e["type"] for e in data["edges"]]
        assert EdgeType.SLOT not in edge_types
        
        # Regular edges should still be present
        assert EdgeType.BACKWARD_REF in edge_types
    
    def test_tier_1_includes_slot_edges(self, graph_with_slot_edges):
        """Tier 1 (detailed) should include slot edges."""
        # Export as JSON at tier 1
        json_output = graph_with_slot_edges.to_json(tier=Tier.DETAILED)
        data = json.loads(json_output)
        
        # Slot edges should be included
        edge_types = [e["type"] for e in data["edges"]]
        assert EdgeType.SLOT in edge_types
    
    def test_tier_0_shows_node_badges(self, graph_with_slot_edges):
        """Tier 0 should include badges when provided."""
        badges = {"container": "[2 slots]"}
        
        # Export as JSON with badges
        json_output = graph_with_slot_edges.to_json(tier=Tier.STRUCTURAL, node_badges=badges)
        data = json.loads(json_output)
        
        # Find the container node and check for badge
        container_node = None
        for node in data["nodes"]:
            if isinstance(node, dict) and node.get("id") == "container":
                container_node = node
                break
        
        assert container_node is not None, "Container node should exist"
        assert container_node.get("badge") == "[2 slots]"


# =============================================================================
# Priority 3 (WARNING) - CLI Commands
# =============================================================================

class TestGraphCommand:
    """Tests for graph CLI command."""
    
    def test_graph_tier_0_default(self, flow_file_with_slots, capsys):
        """Graph command should default to tier 0."""
        args = argparse.Namespace(
            file=str(flow_file_with_slots),
            format="json",
            tier="0"  # cli_manager passes as string
        )
        
        exit_code = graph_command(args)
        captured = capsys.readouterr()
        
        # Should succeed
        assert exit_code == 0
        
        # Parse output
        data = json.loads(captured.out)
        
        # Should be tier 0
        assert data.get("tier") == 0
    
    def test_graph_tier_as_string_casted_to_int(self, flow_file_with_slots, capsys):
        """Graph command should handle tier as string (cli_manager passes strings)."""
        # Test tier 1 as string
        args = argparse.Namespace(
            file=str(flow_file_with_slots),
            format="json",
            tier="1"  # String, not int
        )
        
        exit_code = graph_command(args)
        captured = capsys.readouterr()
        
        assert exit_code == 0
        data = json.loads(captured.out)
        assert data.get("tier") == 1


class TestInspectCommand:
    """Tests for inspect CLI command."""
    
    def test_inspect_node_basic_info(self, flow_file_with_slots, capsys):
        """Inspect should show basic node info including slot_count and slot_badge."""
        args = argparse.Namespace(
            file=str(flow_file_with_slots),
            node="container",
            slots=False
        )
        
        exit_code = inspect_command(args)
        captured = capsys.readouterr()
        
        assert exit_code == 0
        
        data = json.loads(captured.out)
        assert data["success"] is True
        
        node_info = data["node"]
        assert node_info["id"] == "container"
        assert "slot_count" in node_info
        assert "slot_badge" in node_info
        assert node_info["slot_count"] == 3  # header, body, footer
        assert node_info["slot_badge"] == "[3 slots]"
    
    def test_inspect_with_slots_flag(self, flow_file_with_slots, capsys):
        """Inspect with --slots should show slot details."""
        args = argparse.Namespace(
            file=str(flow_file_with_slots),
            node="container",
            slots=True
        )
        
        exit_code = inspect_command(args)
        captured = capsys.readouterr()
        
        assert exit_code == 0
        
        data = json.loads(captured.out)
        assert data["success"] is True
        
        # Should have slots key with details
        assert "slots" in data["node"]
        slots = data["node"]["slots"]
        
        # Should have header, body, footer slots
        assert "header" in slots
        assert "body" in slots
        assert "footer" in slots


class TestDebugCommand:
    """Tests for debug CLI command."""
    
    def test_debug_with_trace_slots(self, flow_file_with_slots, capsys):
        """Debug with --trace-slots should show nodes with slots and assignments."""
        args = argparse.Namespace(
            file=str(flow_file_with_slots),
            trace_slots=True
        )
        
        exit_code = debug_command(args)
        captured = capsys.readouterr()
        
        assert exit_code == 0
        
        data = json.loads(captured.out)
        assert data["success"] is True
        assert data.get("trace_slots") is True
        
        # Should have nodes_with_slots
        nodes_with_slots = data.get("nodes_with_slots", {})
        assert "container" in nodes_with_slots
        assert nodes_with_slots["container"]["slot_count"] == 3
        
        # Should have assignments
        assignments = data.get("assignments", [])
        assert len(assignments) >= 1
        
        # Check for the slot assignment
        targets = [a["target"] for a in assignments]
        assert "container.header" in targets


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
