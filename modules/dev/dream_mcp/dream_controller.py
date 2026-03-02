"""
Dream MCP Controller — Business logic for DREAM planning tools.

This controller provides the implementation for all dream_mcp tools.
``dream_mcp.py`` is a thin wrapper; ALL business logic lives here.

Implemented commands:
- ``dream_tree``: Generate annotated ``_tree.md``
- ``dream_stale``: Flag stale module specs
- ``dream_status``: Sprint dashboard with emergency/active/blocked plans
- ``dream_validate``: Comprehensive gate validation (core + DAG)
- ``dream_impact``: DAG walk showing all plans affected by changes to a plan
- ``dream_history``: Module-indexed change history from State Delta entries
- ``dream_emergency``: Declare emergency priority on a plan
- ``dream_archive``: Move completed/cut plan to ``_completed/YYYY-QN/``

All public methods return ``dict[str, Any]`` with
``{"success": bool, ...}`` pattern.
"""

from __future__ import annotations

import math
import re
import shutil
from collections import deque
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from logger_util import Logger

from .frontmatter_parser import parse_frontmatter_file
from .output_formatter import (
    format_history_report,
    format_impact_report,
    format_stale_report,
    format_status_dashboard,
    format_tree_markdown,
    format_validation_report,
)
from .tree_scanner import scan_module_specs, scan_plan_tree

# Module-level logger for standalone helpers outside DreamController
_logger = Logger(name="dream_controller")

# Framework convention path (DREAM v4.05 §10)
_DAY_DREAM_REL = Path(".agent_plan") / "day_dream"

# Valid plan status bases (DREAM v4.05 §1.8)
_VALID_STATUS_BASES: frozenset[str] = frozenset({
    "TODO", "WIP", "DONE", "BLOCKED", "CUT",
})

# Required frontmatter fields for plan _overview.md (DREAM v4.05 §2.1)
_REQUIRED_PLAN_FIELDS: tuple[str, ...] = (
    "name", "type", "magnitude", "status", "origin", "last_updated",
)

# Valid magnitude values (DREAM v4.05 §1.3)
_VALID_MAGNITUDES: frozenset[str] = frozenset({
    "Trivial", "Light", "Standard", "Heavy", "Epic",
})

# Valid plan type values (DREAM v4.05 §1.5)
_VALID_PLAN_TYPES: frozenset[str] = frozenset({"system", "procedure"})

# Line limits by document type (DREAM v4.05 §2.7)
_LINE_LIMITS: dict[str, int] = {
    "_overview.md": 100,
    "01_executive_summary.md": 150,
    "01_summary.md": 200,
    "02_architecture.md": 200,
    "80_implementation.md": 200,
    "81_module_structure.md": 150,
    "82_cli_commands.md": 150,
}


class DreamController:
    """Controller for DREAM planning MCP operations.

    Follows the ``adhd_controller.py`` pattern: class-based, lazy-init
    friendly, all methods return ``dict[str, Any]``.

    Args:
        workspace_root: Workspace root directory. Defaults to ``Path.cwd()``.
    """

    def __init__(self, workspace_root: Path | str | None = None) -> None:
        self._root = (
            Path(workspace_root).resolve() if workspace_root else Path.cwd().resolve()
        )
        self.logger = Logger(name=self.__class__.__name__)
        self._day_dream_path = self._root / _DAY_DREAM_REL

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def day_dream_path(self) -> Path:
        """Absolute path to the day-dream directory."""
        return self._day_dream_path

    # ------------------------------------------------------------------
    # dream tree
    # ------------------------------------------------------------------

    def dream_tree(self, *, active_only: bool = False) -> dict[str, Any]:
        """Generate ``_tree.md`` — annotated folder tree of the day-dream directory.

        Scans ``.agent_plan/day_dream/`` recursively, reads plan status from
        ``_overview.md`` frontmatter, and writes an annotated tree to
        ``_tree.md`` with a generation timestamp.

        Args:
            active_only: If True, exclude ``_completed/`` and
                ``_archive/`` directories.

        Returns:
            Dict with ``success``, ``tree_path``, ``content``, ``active_only``.
        """
        if not self._day_dream_path.is_dir():
            return {
                "success": False,
                "error": "day_dream_not_found",
                "message": (
                    f"Day-dream directory not found: {self._day_dream_path}"
                ),
            }

        try:
            tree = scan_plan_tree(
                self._day_dream_path, active_only=active_only
            )

            rel_path = str(_DAY_DREAM_REL).replace("\\", "/")
            content = format_tree_markdown(tree, rel_path)

            # Write _tree.md (the only file dream tree mutates)
            tree_path = self._day_dream_path / "_tree.md"
            tree_path.write_text(content, encoding="utf-8")

            self.logger.info(f"Generated _tree.md at {tree_path}")

            return {
                "success": True,
                "tree_path": str(tree_path.relative_to(self._root)),
                "content": content,
                "active_only": active_only,
            }
        except Exception as exc:  # FALLBACK: MCP tools must return error dicts, not crash the server — permanent
            self.logger.error(f"Failed to generate tree: {exc}")
            return {
                "success": False,
                "error": "tree_generation_failed",
                "message": str(exc),
            }

    # ------------------------------------------------------------------
    # dream stale
    # ------------------------------------------------------------------

    def dream_stale(
        self,
        *,
        weeks: int = 4,
        module: str | None = None,
    ) -> dict[str, Any]:
        """Flag module specs where ``last_updated`` exceeds staleness threshold.

        Scans ``modules/*.md`` files across all plan directories, parses
        their ``last_updated`` frontmatter field, and identifies those
        exceeding the staleness threshold.

        Args:
            weeks: Number of weeks threshold for staleness (default: 4).
                ``weeks=0`` flags everything (threshold is zero days).
            module: Optional module name to filter to a single module.

        Returns:
            Dict with ``success``, ``stale`` list, ``total_scanned``,
            ``threshold_weeks``, and ``report``.
        """
        if not self._day_dream_path.is_dir():
            return {
                "success": False,
                "error": "day_dream_not_found",
                "message": (
                    f"Day-dream directory not found: {self._day_dream_path}"
                ),
            }

        try:
            all_specs = scan_module_specs(self._day_dream_path)

            # Optional module filter
            if module:
                all_specs = [s for s in all_specs if s["module"] == module]
                if not all_specs:
                    return {
                        "success": True,
                        "stale": [],
                        "total_scanned": 0,
                        "threshold_weeks": weeks,
                        "message": f"No module spec found for '{module}'",
                        "report": f"No module spec found for '{module}'.",
                    }

            threshold = timedelta(weeks=weeks)
            now = datetime.now(timezone.utc).date()
            stale: list[dict[str, Any]] = []

            for spec in all_specs:
                last_updated_raw = spec.get("last_updated")
                spec_rel_path = str(spec["path"].relative_to(self._root))

                if last_updated_raw is None:
                    # Missing last_updated → always stale
                    stale.append({
                        "module": spec["module"],
                        "last_updated": "MISSING",
                        "plan": spec["plan"],
                        "days_stale": "N/A",
                        "path": spec_rel_path,
                    })
                    continue

                last_date = _parse_date(last_updated_raw)
                if last_date is None:
                    stale.append({
                        "module": spec["module"],
                        "last_updated": str(last_updated_raw),
                        "plan": spec["plan"],
                        "days_stale": "PARSE_ERROR",
                        "path": spec_rel_path,
                    })
                    continue

                age = now - last_date
                if age > threshold:
                    stale.append({
                        "module": spec["module"],
                        "last_updated": str(last_date),
                        "plan": spec["plan"],
                        "days_stale": age.days,
                        "path": spec_rel_path,
                    })

            report = format_stale_report(stale, weeks, len(all_specs))

            self.logger.info(
                f"Stale check: {len(stale)}/{len(all_specs)} modules stale "
                f"(threshold: {weeks} weeks)"
            )

            return {
                "success": True,
                "stale": stale,
                "total_scanned": len(all_specs),
                "threshold_weeks": weeks,
                "report": report,
            }
        except Exception as exc:  # FALLBACK: MCP tools must return error dicts, not crash the server — permanent
            self.logger.error(f"Failed stale check: {exc}")
            return {
                "success": False,
                "error": "stale_check_failed",
                "message": str(exc),
            }

    # ------------------------------------------------------------------
    # dream status
    # ------------------------------------------------------------------

    def dream_status(self, *, gaps: bool = False) -> dict[str, Any]:
        """Display current sprint, active/blocked/emergency plans, aggregate warnings.

        Scans all ``_overview.md`` frontmatter across the plan tree and
        categorizes plans by status. Emergency plans appear first (ordered
        by ``emergency_declared_at``), then active, then blocked, then
        remaining categories.

        Args:
            gaps: If True, include knowledge gap aggregation in the report.

        Returns:
            Dict with ``success``, ``plans`` (categorized), ``summary``
            (counts), ``knowledge_gaps`` (if requested), and ``report``
            (formatted dashboard string).
        """
        if not self._day_dream_path.is_dir():
            return {
                "success": False,
                "error": "day_dream_not_found",
                "message": (
                    f"Day-dream directory not found: {self._day_dream_path}"
                ),
            }

        try:
            plans = self._collect_plan_summaries()
            categorized = self._categorize_plans(plans)
            knowledge_gaps = self._collect_knowledge_gaps(plans) if gaps else []

            # Summary counts
            summary: dict[str, int] = {
                "total": len(plans),
                "emergency": len(categorized.get("emergency", [])),
                "active": len(categorized.get("active", [])),
                "blocked": len(categorized.get("blocked", [])),
                "todo": len(categorized.get("todo", [])),
                "done": len(categorized.get("done", [])),
                "cut": len(categorized.get("cut", [])),
            }

            report = format_status_dashboard(
                categorized, summary, knowledge_gaps, gaps=gaps,
            )

            self.logger.info(
                f"Status: {summary['total']} plans — "
                f"{summary['emergency']} emergency, "
                f"{summary['active']} active, "
                f"{summary['blocked']} blocked"
            )

            result: dict[str, Any] = {
                "success": True,
                "plans": categorized,
                "summary": summary,
                "report": report,
            }
            if gaps:
                result["knowledge_gaps"] = knowledge_gaps
            return result

        except Exception as exc:  # FALLBACK: MCP tools must return error dicts, not crash the server — permanent
            self.logger.error(f"Failed status check: {exc}")
            return {
                "success": False,
                "error": "status_check_failed",
                "message": str(exc),
            }

    # ------------------------------------------------------------------
    # dream validate
    # ------------------------------------------------------------------

    def dream_validate(
        self,
        *,
        plan: str | None = None,
    ) -> dict[str, Any]:
        """Comprehensive gate validation — check all convention enforcement rules.

        Runs core checks (frontmatter, status syntax, line limits, missing
        sections) and DAG checks (cycle detection, bidirectional consistency,
        orphaned references) across all plans or a specific plan.

        Args:
            plan: Optional plan directory name to scope validation.
                If None, validates all plans under day-dream.

        Returns:
            Dict with ``success``, ``errors`` list, ``warnings`` list,
            ``error_count``, ``warning_count``, ``valid`` bool, and
            ``report`` (formatted validation report string).
        """
        if not self._day_dream_path.is_dir():
            return {
                "success": False,
                "error": "day_dream_not_found",
                "message": (
                    f"Day-dream directory not found: {self._day_dream_path}"
                ),
            }

        try:
            errors: list[dict[str, str]] = []
            warnings: list[dict[str, str]] = []

            # Determine scope — all plans or a specific one
            plan_dirs = self._get_plan_dirs(plan)
            if plan and not plan_dirs:
                return {
                    "success": True,
                    "errors": [],
                    "warnings": [],
                    "error_count": 0,
                    "warning_count": 0,
                    "valid": True,
                    "message": f"No plan directory found for '{plan}'",
                    "report": f"No plan directory found for '{plan}'.",
                }

            # --- Core validation checks ---
            for plan_dir in plan_dirs:
                self._validate_plan_dir(plan_dir, errors, warnings)

            # --- DAG validation checks (across all scanned plans) ---
            self._validate_dependency_dag(plan_dirs, errors, warnings)

            valid = len(errors) == 0
            report = format_validation_report(errors, warnings)

            self.logger.info(
                f"Validate: {len(errors)} errors, {len(warnings)} warnings "
                f"— {'PASS' if valid else 'FAIL'}"
            )

            return {
                "success": True,
                "errors": errors,
                "warnings": warnings,
                "error_count": len(errors),
                "warning_count": len(warnings),
                "valid": valid,
                "report": report,
            }

        except Exception as exc:  # FALLBACK: MCP tools must return error dicts, not crash the server — permanent
            self.logger.error(f"Failed validation: {exc}")
            return {
                "success": False,
                "error": "validation_failed",
                "message": str(exc),
            }

    # ------------------------------------------------------------------
    # dream impact
    # ------------------------------------------------------------------

    def dream_impact(
        self,
        *,
        plan_id: str,
        modules: bool = False,
    ) -> dict[str, Any]:
        """DAG walk showing all plans affected by changes to ``plan_id``.

        Traverses ``depends_on`` / ``blocks`` relationships to find all
        direct and transitive dependents of the given plan. Optionally
        includes affected modules from State Delta and Module Index.

        Args:
            plan_id: Plan directory name (e.g. ``"SP01_dream_v405_implementation"``).
            modules: If True, include affected modules in the report.

        Returns:
            Dict with ``success``, ``plan_id``, ``direct_dependents``,
            ``transitive_dependents``, ``affected_modules`` (if requested),
            and ``report`` (formatted impact report string).
        """
        if not self._day_dream_path.is_dir():
            return {
                "success": False,
                "error": "day_dream_not_found",
                "message": (
                    f"Day-dream directory not found: {self._day_dream_path}"
                ),
            }

        try:
            plan_dirs = self._get_plan_dirs(plan_filter=None)
            known_names = {d.name for d in plan_dirs}

            if plan_id not in known_names:
                return {
                    "success": False,
                    "error": "plan_not_found",
                    "message": f"Plan '{plan_id}' not found in day-dream directory",
                }

            # Build dependency graph from all plans
            graph = self._build_dependency_graph(plan_dirs)

            # Direct dependents: plans whose depends_on includes plan_id
            direct: list[str] = [
                name for name, edges in graph.items()
                if plan_id in edges["depends_on"]
            ]

            # Transitive dependents via BFS on reverse edges
            transitive = self._transitive_dependents(plan_id, graph)
            # Remove direct dependents and self from transitive set
            transitive_only = sorted(
                transitive - {plan_id} - set(direct)
            )

            # Collect plan summaries for display
            plan_summaries = self._collect_plan_summaries()
            summary_map: dict[str, dict[str, Any]] = {
                p["name"]: p for p in plan_summaries
            }

            direct_details = [
                summary_map[n] for n in sorted(direct) if n in summary_map
            ]
            transitive_details = [
                summary_map[n] for n in transitive_only if n in summary_map
            ]

            # Affected modules (from module specs referencing this plan)
            affected_modules: list[dict[str, Any]] = []
            if modules:
                affected_modules = self._collect_affected_modules(
                    plan_id, plan_dirs,
                )

            # Invalidation warning — all plans that could be affected
            all_affected = sorted(set(direct) | set(transitive_only))

            report = format_impact_report(
                plan_id=plan_id,
                direct_dependents=direct_details,
                transitive_dependents=transitive_details,
                affected_modules=affected_modules,
                all_affected=all_affected,
                show_modules=modules,
            )

            self.logger.info(
                f"Impact: {plan_id} — {len(direct)} direct, "
                f"{len(transitive_only)} transitive dependents"
            )

            result: dict[str, Any] = {
                "success": True,
                "plan_id": plan_id,
                "direct_dependents": [d["name"] for d in direct_details],
                "transitive_dependents": [t["name"] for t in transitive_details],
                "all_affected": all_affected,
                "report": report,
            }
            if modules:
                result["affected_modules"] = affected_modules
            return result

        except Exception as exc:  # FALLBACK: MCP tools must return error dicts, not crash the server — permanent
            self.logger.error(f"Failed impact analysis: {exc}")
            return {
                "success": False,
                "error": "impact_analysis_failed",
                "message": str(exc),
            }

    # ------------------------------------------------------------------
    # dream history
    # ------------------------------------------------------------------

    def dream_history(self, *, module_name: str) -> dict[str, Any]:
        """Generate module-indexed change history from State Delta entries.

        Scans State Deltas from root ``_overview.md`` and
        ``_state_deltas_archive.md`` for entries referencing the given
        module name. Returns a chronological change history table.

        Args:
            module_name: Module name to search for (e.g. ``"dream_mcp"``).

        Returns:
            Dict with ``success``, ``module``, ``entries`` list, and
            ``report`` (formatted history report string).
        """
        if not self._day_dream_path.is_dir():
            return {
                "success": False,
                "error": "day_dream_not_found",
                "message": (
                    f"Day-dream directory not found: {self._day_dream_path}"
                ),
            }

        try:
            entries: list[dict[str, str]] = []

            # Scan root _overview.md State Deltas
            overview_path = self._day_dream_path / "_overview.md"
            if overview_path.is_file():
                entries.extend(
                    _parse_state_deltas_for_module(overview_path, module_name)
                )

            # Scan archive file if it exists
            archive_path = self._day_dream_path / "_state_deltas_archive.md"
            if archive_path.is_file():
                entries.extend(
                    _parse_state_deltas_for_module(archive_path, module_name)
                )

            # Sort chronologically (archive entries first, then overview)
            # Since archive holds older entries, reverse to get oldest-first
            # Entries are already in file order; archive entries come second
            # but should be chronologically earlier. Re-sort by date string.
            entries.sort(key=lambda e: e.get("date", ""))

            report = format_history_report(module_name, entries)

            self.logger.info(
                f"History: {module_name} — {len(entries)} change entries found"
            )

            return {
                "success": True,
                "module": module_name,
                "entries": entries,
                "entry_count": len(entries),
                "report": report,
            }

        except Exception as exc:  # FALLBACK: MCP tools must return error dicts, not crash the server — permanent
            self.logger.error(f"Failed history lookup: {exc}")
            return {
                "success": False,
                "error": "history_lookup_failed",
                "message": str(exc),
            }

    # ------------------------------------------------------------------
    # dream emergency
    # ------------------------------------------------------------------

    def dream_emergency(
        self,
        *,
        plan_id: str,
        reason: str,
    ) -> dict[str, Any]:
        """Declare emergency priority on a plan.

        Sets ``priority: emergency``, ``emergency_declared_at:``, and
        updates ``last_updated`` in the plan's ``_overview.md`` frontmatter.

        Uses write-then-rename atomic pattern for safety.

        Args:
            plan_id: Plan directory name.
            reason: Human-readable reason for the emergency declaration.

        Returns:
            Dict with ``success``, ``plan_id``, ``emergency_declared_at``,
            and ``message``.
        """
        if not self._day_dream_path.is_dir():
            return {
                "success": False,
                "error": "day_dream_not_found",
                "message": (
                    f"Day-dream directory not found: {self._day_dream_path}"
                ),
            }

        try:
            plan_dir = self._day_dream_path / plan_id
            if not plan_dir.is_dir():
                return {
                    "success": False,
                    "error": "plan_not_found",
                    "message": f"Plan directory '{plan_id}' not found",
                }

            overview_path = plan_dir / "_overview.md"
            if not overview_path.is_file():
                return {
                    "success": False,
                    "error": "overview_not_found",
                    "message": f"No _overview.md in '{plan_id}'",
                }

            fm = parse_frontmatter_file(overview_path)
            if fm is None:
                return {
                    "success": False,
                    "error": "frontmatter_parse_error",
                    "message": f"Could not parse frontmatter in '{plan_id}/_overview.md'",
                }

            # Precondition: plan should not already be DONE or CUT
            status_base = str(fm.get("status", "")).split(":")[0]
            if status_base in ("DONE", "CUT"):
                return {
                    "success": False,
                    "error": "invalid_status_for_emergency",
                    "message": (
                        f"Cannot declare emergency on {status_base} plan "
                        f"'{plan_id}'"
                    ),
                }

            now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
            today_iso = date.today().isoformat()

            # Read the raw file content
            raw_content = overview_path.read_text(encoding="utf-8")

            # Update frontmatter fields via text replacement
            updated_content = _update_frontmatter_field(
                raw_content, "priority", "emergency",
            )
            updated_content = _update_frontmatter_field(
                updated_content, "emergency_declared_at", now_iso,
            )
            updated_content = _update_frontmatter_field(
                updated_content, "emergency_reason", reason,
            )
            updated_content = _update_frontmatter_field(
                updated_content, "last_updated", today_iso,
            )

            # Atomic write: write to temp, then rename
            tmp_path = overview_path.with_suffix(".md.tmp")
            tmp_path.write_text(updated_content, encoding="utf-8")
            tmp_path.rename(overview_path)

            self.logger.info(
                f"Emergency declared on '{plan_id}' at {now_iso}: {reason}"
            )

            return {
                "success": True,
                "plan_id": plan_id,
                "emergency_declared_at": now_iso,
                "reason": reason,
                "message": (
                    f"Emergency declared on '{plan_id}'. "
                    f"priority=emergency, declared_at={now_iso}"
                ),
            }

        except Exception as exc:  # FALLBACK: MCP tools must return error dicts, not crash the server — permanent
            self.logger.error(f"Failed emergency declaration: {exc}")
            return {
                "success": False,
                "error": "emergency_declaration_failed",
                "message": str(exc),
            }

    # ------------------------------------------------------------------
    # dream archive
    # ------------------------------------------------------------------

    def dream_archive(self, *, plan_id: str) -> dict[str, Any]:
        """Move a completed or cut plan to ``_completed/YYYY-QN/``.

        Only works on plans with status DONE or CUT. Creates the
        ``_completed/`` and quarter directories as needed.

        Uses ``shutil.move`` for the directory relocation.

        Args:
            plan_id: Plan directory name.

        Returns:
            Dict with ``success``, ``plan_id``, ``archived_to``, and ``message``.
        """
        if not self._day_dream_path.is_dir():
            return {
                "success": False,
                "error": "day_dream_not_found",
                "message": (
                    f"Day-dream directory not found: {self._day_dream_path}"
                ),
            }

        try:
            plan_dir = self._day_dream_path / plan_id
            if not plan_dir.is_dir():
                return {
                    "success": False,
                    "error": "plan_not_found",
                    "message": f"Plan directory '{plan_id}' not found",
                }

            overview_path = plan_dir / "_overview.md"
            if not overview_path.is_file():
                return {
                    "success": False,
                    "error": "overview_not_found",
                    "message": f"No _overview.md in '{plan_id}'",
                }

            fm = parse_frontmatter_file(overview_path)
            if fm is None:
                return {
                    "success": False,
                    "error": "frontmatter_parse_error",
                    "message": f"Could not parse frontmatter in '{plan_id}/_overview.md'",
                }

            # Precondition: plan must be DONE or CUT
            status_base = str(fm.get("status", "")).split(":")[0]
            if status_base not in ("DONE", "CUT"):
                return {
                    "success": False,
                    "error": "invalid_status_for_archive",
                    "message": (
                        f"Cannot archive plan '{plan_id}' with status "
                        f"'{fm.get('status')}' — must be DONE or CUT"
                    ),
                }

            # Determine quarter directory (YYYY-QN)
            quarter_dir_name = _current_quarter_dirname()
            completed_path = self._day_dream_path / "_completed"
            quarter_path = completed_path / quarter_dir_name
            dest_path = quarter_path / plan_id

            if dest_path.exists():
                return {
                    "success": False,
                    "error": "archive_destination_exists",
                    "message": (
                        f"Archive destination already exists: "
                        f"{dest_path.relative_to(self._root)}"
                    ),
                }

            # Create directories as needed
            quarter_path.mkdir(parents=True, exist_ok=True)

            # Move the plan directory
            shutil.move(str(plan_dir), str(dest_path))

            archived_to = str(dest_path.relative_to(self._root))
            self.logger.info(f"Archived '{plan_id}' to {archived_to}")

            return {
                "success": True,
                "plan_id": plan_id,
                "archived_to": archived_to,
                "message": f"Plan '{plan_id}' archived to {archived_to}",
            }

        except Exception as exc:  # FALLBACK: MCP tools must return error dicts, not crash the server — permanent
            self.logger.error(f"Failed archive: {exc}")
            return {
                "success": False,
                "error": "archive_failed",
                "message": str(exc),
            }

    # ------------------------------------------------------------------
    # Status helpers
    # ------------------------------------------------------------------

    def _collect_plan_summaries(self) -> list[dict[str, Any]]:
        """Collect summary info for all plans under day-dream.

        Returns:
            List of dicts with plan name, status, priority, depends_on,
            blocks, knowledge_gaps, emergency_declared_at, and path.
        """
        plans: list[dict[str, Any]] = []

        for entry in sorted(self._day_dream_path.iterdir()):
            if not entry.is_dir():
                continue
            if entry.name.startswith(("_", ".")):
                continue

            overview = entry / "_overview.md"
            if not overview.is_file():
                continue

            fm = parse_frontmatter_file(overview)
            if fm is None:
                continue

            status_raw = fm.get("status", "")
            status_base = str(status_raw).split(":")[0] if status_raw else ""
            priority = fm.get("priority", "normal")

            plans.append({
                "name": entry.name,
                "status": str(status_raw),
                "status_base": status_base,
                "priority": str(priority),
                "type": fm.get("type", "unknown"),
                "magnitude": fm.get("magnitude", "unknown"),
                "depends_on": fm.get("depends_on", []) or [],
                "blocks": fm.get("blocks", []) or [],
                "knowledge_gaps": fm.get("knowledge_gaps", []) or [],
                "emergency_declared_at": fm.get("emergency_declared_at"),
                "path": str(entry.relative_to(self._root)),
            })

        return plans

    def _categorize_plans(
        self,
        plans: list[dict[str, Any]],
    ) -> dict[str, list[dict[str, Any]]]:
        """Categorize plans by status into ordered buckets.

        Emergency plans are sorted by ``emergency_declared_at`` (earliest first).

        Args:
            plans: List of plan summary dicts.

        Returns:
            Dict keyed by category: emergency, active, blocked, todo, done, cut.
        """
        categories: dict[str, list[dict[str, Any]]] = {
            "emergency": [],
            "active": [],
            "blocked": [],
            "todo": [],
            "done": [],
            "cut": [],
        }

        for p in plans:
            if p["priority"] == "emergency":
                categories["emergency"].append(p)
            elif p["status_base"] == "WIP":
                categories["active"].append(p)
            elif p["status_base"] == "BLOCKED":
                categories["blocked"].append(p)
            elif p["status_base"] == "TODO":
                categories["todo"].append(p)
            elif p["status_base"] == "DONE":
                categories["done"].append(p)
            elif p["status_base"] == "CUT":
                categories["cut"].append(p)
            else:
                # Unknown status → treat as todo
                categories["todo"].append(p)

        # Sort emergencies by declaration time (earliest first)
        categories["emergency"].sort(
            key=lambda p: p.get("emergency_declared_at") or "",
        )

        return categories

    @staticmethod
    def _collect_knowledge_gaps(
        plans: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Aggregate knowledge gaps across all plans.

        Args:
            plans: List of plan summary dicts.

        Returns:
            List of dicts with ``plan`` name and ``gap`` description.
        """
        gaps: list[dict[str, Any]] = []
        for p in plans:
            for gap in p.get("knowledge_gaps", []):
                gaps.append({"plan": p["name"], "gap": str(gap)})
        return gaps

    # ------------------------------------------------------------------
    # Validate helpers — plan directory scanning
    # ------------------------------------------------------------------

    def _get_plan_dirs(
        self,
        plan_filter: str | None,
    ) -> list[Path]:
        """Get plan directories to validate.

        Args:
            plan_filter: Optional plan name to filter to.

        Returns:
            List of plan directory paths.
        """
        plan_dirs: list[Path] = []

        for entry in sorted(self._day_dream_path.iterdir()):
            if not entry.is_dir():
                continue
            if entry.name.startswith(("_", ".")):
                continue
            overview = entry / "_overview.md"
            if not overview.is_file():
                continue

            if plan_filter and entry.name != plan_filter:
                continue

            plan_dirs.append(entry)

        return plan_dirs

    # ------------------------------------------------------------------
    # Impact helpers — DAG traversal
    # ------------------------------------------------------------------

    def _build_dependency_graph(
        self,
        plan_dirs: list[Path],
    ) -> dict[str, dict[str, list[str]]]:
        """Build the dependency graph from plan frontmatter.

        Args:
            plan_dirs: List of plan directory paths.

        Returns:
            Dict mapping plan_name to ``{"depends_on": [...], "blocks": [...]}``.
        """
        graph: dict[str, dict[str, list[str]]] = {}

        for plan_dir in plan_dirs:
            name = plan_dir.name
            overview = plan_dir / "_overview.md"
            fm = parse_frontmatter_file(overview)
            if fm is None:
                graph[name] = {"depends_on": [], "blocks": []}
                continue

            depends_on = fm.get("depends_on", []) or []
            blocks = fm.get("blocks", []) or []

            if isinstance(depends_on, str):
                depends_on = [depends_on]
            if isinstance(blocks, str):
                blocks = [blocks]

            graph[name] = {
                "depends_on": [str(d) for d in depends_on],
                "blocks": [str(b) for b in blocks],
            }

        return graph

    @staticmethod
    def _transitive_dependents(
        plan_id: str,
        graph: dict[str, dict[str, list[str]]],
    ) -> set[str]:
        """Find all transitive dependents of a plan via BFS.

        A dependent is a plan whose ``depends_on`` includes ``plan_id``
        or any of its transitive dependents.

        Args:
            plan_id: The source plan to find dependents of.
            graph: Dependency graph from ``_build_dependency_graph``.

        Returns:
            Set of all transitive dependent plan names (excludes ``plan_id``).
        """
        # Build reverse graph: plan → plans that depend on it
        reverse: dict[str, list[str]] = {name: [] for name in graph}
        for name, edges in graph.items():
            for dep in edges["depends_on"]:
                if dep in reverse:
                    reverse[dep].append(name)

        # BFS from plan_id through reverse edges
        visited: set[str] = set()
        queue: deque[str] = deque([plan_id])
        while queue:
            current = queue.popleft()
            for dependent in reverse.get(current, []):
                if dependent not in visited:
                    visited.add(dependent)
                    queue.append(dependent)

        return visited

    def _collect_affected_modules(
        self,
        plan_id: str,
        plan_dirs: list[Path],
    ) -> list[dict[str, Any]]:
        """Collect modules affected by a plan from module spec files.

        Scans module spec files for references to ``plan_id`` in
        ``modified_by_plans`` or matching ``origin_plan`` fields.

        Args:
            plan_id: Plan name to search for.
            plan_dirs: All plan directories.

        Returns:
            List of dicts with ``module``, ``origin``, ``modified_by``.
        """
        affected: list[dict[str, Any]] = []
        all_specs = scan_module_specs(self._day_dream_path)

        for spec in all_specs:
            origin = spec.get("plan", "")
            modified_by = spec.get("modified_by_plans", []) or []
            # Check if the plan_id matches the origin or is in modified_by
            # Use partial match: SP01 matches SP01_dream_v405_implementation
            is_origin = (
                origin == plan_id
                or plan_id.startswith(origin)
                or origin.startswith(plan_id)
            )
            is_modifier = any(
                plan_id == m or plan_id.startswith(m) or m.startswith(plan_id)
                for m in modified_by
            )

            if is_origin or is_modifier:
                affected.append({
                    "module": spec["module"],
                    "origin": origin,
                    "modified_by": modified_by,
                })

        return affected

    # ------------------------------------------------------------------
    # Validate helpers — core checks
    # ------------------------------------------------------------------

    def _validate_plan_dir(
        self,
        plan_dir: Path,
        errors: list[dict[str, str]],
        warnings: list[dict[str, str]],
    ) -> None:
        """Run core validation checks on a single plan directory.

        Checks frontmatter completeness, status syntax, line limits,
        conditional field requirements, and required sections.

        Args:
            plan_dir: Path to the plan directory.
            errors: Accumulator for ERROR-level issues.
            warnings: Accumulator for WARNING-level issues.
        """
        plan_name = plan_dir.name
        overview_path = plan_dir / "_overview.md"

        fm = parse_frontmatter_file(overview_path)

        if fm is None:
            errors.append({
                "plan": plan_name,
                "check": "frontmatter_missing",
                "message": f"No valid frontmatter in {plan_name}/_overview.md",
            })
            return

        # --- Required fields ---
        for field_name in _REQUIRED_PLAN_FIELDS:
            if field_name not in fm or fm[field_name] is None:
                errors.append({
                    "plan": plan_name,
                    "check": "required_field_missing",
                    "message": (
                        f"Required field '{field_name}' missing "
                        f"in {plan_name}/_overview.md"
                    ),
                })

        # --- Status syntax ---
        status_raw = fm.get("status")
        if status_raw is not None:
            self._validate_status_syntax(
                str(status_raw), plan_name, "_overview.md", errors,
            )

        # --- Magnitude validity ---
        magnitude = fm.get("magnitude")
        if magnitude is not None and str(magnitude) not in _VALID_MAGNITUDES:
            errors.append({
                "plan": plan_name,
                "check": "invalid_magnitude",
                "message": (
                    f"Invalid magnitude '{magnitude}' in {plan_name}/_overview.md "
                    f"— valid: {', '.join(sorted(_VALID_MAGNITUDES))}"
                ),
            })

        # --- Type validity ---
        plan_type = fm.get("type")
        if plan_type is not None and str(plan_type) not in _VALID_PLAN_TYPES:
            errors.append({
                "plan": plan_name,
                "check": "invalid_type",
                "message": (
                    f"Invalid type '{plan_type}' in {plan_name}/_overview.md "
                    f"— valid: {', '.join(sorted(_VALID_PLAN_TYPES))}"
                ),
            })

        # --- Conditional: emergency_declared_at when priority=emergency ---
        if fm.get("priority") == "emergency":
            if not fm.get("emergency_declared_at"):
                errors.append({
                    "plan": plan_name,
                    "check": "emergency_no_timestamp",
                    "message": (
                        f"priority=emergency but 'emergency_declared_at' "
                        f"missing in {plan_name}/_overview.md"
                    ),
                })

        # --- Conditional: invalidation fields ---
        if fm.get("invalidated_by"):
            if not fm.get("invalidation_scope"):
                errors.append({
                    "plan": plan_name,
                    "check": "invalidation_scope_missing",
                    "message": (
                        f"'invalidated_by' set but 'invalidation_scope' "
                        f"missing in {plan_name}/_overview.md"
                    ),
                })

        # --- Line limit checks ---
        self._validate_line_limits(plan_dir, errors)

        # --- Recommended: depends_on / blocks ---
        # If a plan references another plan in depends_on, log presence
        # (bidirectional consistency is checked in DAG validation)

        # --- Recurse into child plans ---
        self._validate_child_plans(plan_dir, errors, warnings)

    def _validate_child_plans(
        self,
        plan_dir: Path,
        errors: list[dict[str, str]],
        warnings: list[dict[str, str]],
    ) -> None:
        """Validate child plan directories (sub-phases like p01/, p02/).

        Args:
            plan_dir: Parent plan directory.
            errors: Accumulator for ERROR-level issues.
            warnings: Accumulator for WARNING-level issues.
        """
        plan_name = plan_dir.name

        for entry in sorted(plan_dir.iterdir()):
            if not entry.is_dir():
                continue
            if entry.name.startswith(("_", ".")):
                continue
            # Only validate child dirs that have _overview.md (they are plans)
            child_overview = entry / "_overview.md"
            if not child_overview.is_file():
                continue

            child_fm = parse_frontmatter_file(child_overview)
            child_name = f"{plan_name}/{entry.name}"

            if child_fm is None:
                errors.append({
                    "plan": child_name,
                    "check": "frontmatter_missing",
                    "message": (
                        f"No valid frontmatter in {child_name}/_overview.md"
                    ),
                })
                continue

            # Required fields on child plans
            for field_name in _REQUIRED_PLAN_FIELDS:
                if field_name not in child_fm or child_fm[field_name] is None:
                    errors.append({
                        "plan": child_name,
                        "check": "required_field_missing",
                        "message": (
                            f"Required field '{field_name}' missing "
                            f"in {child_name}/_overview.md"
                        ),
                    })

            # Status syntax on children
            child_status = child_fm.get("status")
            if child_status is not None:
                self._validate_status_syntax(
                    str(child_status), child_name, "_overview.md", errors,
                )

    @staticmethod
    def _validate_status_syntax(
        status: str,
        plan_name: str,
        file_name: str,
        errors: list[dict[str, str]],
    ) -> None:
        """Validate that a status value conforms to DREAM v4.05 §1.8.

        Valid forms:
        - ``TODO``, ``WIP``, ``DONE``, ``CUT``
        - ``BLOCKED:kebab-case-reason``
        - ``DONE:invalidated-by:XXnn``

        Args:
            status: Raw status string.
            plan_name: Plan name for error reporting.
            file_name: File name context for error reporting.
            errors: Accumulator for ERROR-level issues.
        """
        base = status.split(":")[0]
        if base not in _VALID_STATUS_BASES:
            errors.append({
                "plan": plan_name,
                "check": "invalid_status",
                "message": (
                    f"Invalid status '{status}' in {plan_name}/{file_name} "
                    f"— valid bases: {', '.join(sorted(_VALID_STATUS_BASES))}"
                ),
            })
            return

        # BLOCKED must have a reason suffix
        if base == "BLOCKED" and ":" not in status:
            errors.append({
                "plan": plan_name,
                "check": "blocked_no_reason",
                "message": (
                    f"BLOCKED status missing reason in {plan_name}/{file_name} "
                    f"— expected BLOCKED:kebab-case-reason"
                ),
            })

    def _validate_line_limits(
        self,
        plan_dir: Path,
        errors: list[dict[str, str]],
    ) -> None:
        """Check line limits for known document types in a plan directory.

        Args:
            plan_dir: Plan directory to check.
            errors: Accumulator for ERROR-level issues.
        """
        plan_name = plan_dir.name

        for filename, limit in _LINE_LIMITS.items():
            file_path = plan_dir / filename
            if not file_path.is_file():
                continue

            try:
                line_count = len(
                    file_path.read_text(encoding="utf-8").splitlines()
                )
                if line_count > limit:
                    errors.append({
                        "plan": plan_name,
                        "check": "line_limit_exceeded",
                        "message": (
                            f"{plan_name}/{filename}: {line_count} lines "
                            f"exceeds limit of {limit}"
                        ),
                    })
            except OSError as exc:
                self.logger.debug(f"Could not read {file_path}: {exc}")

    # ------------------------------------------------------------------
    # Validate helpers — DAG checks
    # ------------------------------------------------------------------

    def _validate_dependency_dag(
        self,
        plan_dirs: list[Path],
        errors: list[dict[str, str]],
        warnings: list[dict[str, str]],
    ) -> None:
        """Validate the dependency graph across all plans.

        Checks for:
        1. Cycles in ``depends_on`` / ``blocks`` relationships
        2. Bidirectional consistency (A depends_on B → B should block A)
        3. Orphaned references (references to non-existent plans)

        Args:
            plan_dirs: List of plan directory paths.
            errors: Accumulator for ERROR-level issues.
            warnings: Accumulator for WARNING-level issues.
        """
        graph = self._build_dependency_graph(plan_dirs)
        known_plans: set[str] = set(graph.keys())

        # --- Check 1: Orphaned references ---
        for plan_name, edges in graph.items():
            for dep in edges["depends_on"]:
                if dep not in known_plans:
                    warnings.append({
                        "plan": plan_name,
                        "check": "orphaned_depends_on",
                        "message": (
                            f"{plan_name} depends_on '{dep}' "
                            f"which does not exist as a plan"
                        ),
                    })
            for blk in edges["blocks"]:
                if blk not in known_plans:
                    warnings.append({
                        "plan": plan_name,
                        "check": "orphaned_blocks",
                        "message": (
                            f"{plan_name} blocks '{blk}' "
                            f"which does not exist as a plan"
                        ),
                    })

        # --- Check 2: Bidirectional consistency ---
        for plan_name, edges in graph.items():
            for dep in edges["depends_on"]:
                if dep in graph:
                    dep_blocks = graph[dep].get("blocks", [])
                    if plan_name not in dep_blocks:
                        warnings.append({
                            "plan": plan_name,
                            "check": "bidirectional_inconsistency",
                            "message": (
                                f"{plan_name} depends_on '{dep}', "
                                f"but {dep} does not list {plan_name} in blocks"
                            ),
                        })

        # --- Check 3: Cycle detection (DFS-based) ---
        # Build forward adjacency: plan → [plans it depends on]
        forward: dict[str, list[str]] = {}
        for plan_name, edges in graph.items():
            forward[plan_name] = edges["depends_on"]

        cycle = _detect_cycle(forward)
        if cycle:
            cycle_str = " → ".join(cycle)
            errors.append({
                "plan": cycle[0],
                "check": "dependency_cycle",
                "message": f"Dependency cycle detected: {cycle_str}",
            })


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_date(value: Any) -> date | None:
    """Parse a date from a frontmatter value.

    Handles ``datetime.date`` objects (auto-parsed by PyYAML),
    ``datetime.datetime`` objects, and ISO-format date strings
    (``YYYY-MM-DD``).

    Args:
        value: Raw frontmatter date value.

    Returns:
        Parsed ``date``, or None if unparseable.
    """
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def _detect_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    """Detect a cycle in a directed graph using iterative DFS.

    Args:
        graph: Adjacency dict mapping node → list of successor nodes.
            Nodes not in the dict are treated as having no successors.

    Returns:
        List of node names forming the cycle (e.g. ``["A", "B", "A"]``),
        or None if the graph is acyclic.
    """
    # States: 0 = unvisited, 1 = in-progress, 2 = done
    state: dict[str, int] = {node: 0 for node in graph}
    parent: dict[str, str | None] = {}

    for start in graph:
        if state[start] != 0:
            continue

        stack: list[tuple[str, int]] = [(start, 0)]
        parent[start] = None

        while stack:
            node, idx = stack.pop()
            neighbors = graph.get(node, [])

            if idx == 0:
                state[node] = 1  # Mark in-progress

            if idx < len(neighbors):
                # Push current node back with incremented index
                stack.append((node, idx + 1))
                neighbor = neighbors[idx]

                if neighbor not in state:
                    # Node not in graph keys — skip
                    continue

                if state[neighbor] == 1:
                    # Found a cycle — reconstruct path
                    cycle = [node]
                    current = node
                    while current != neighbor:
                        current = parent.get(current)  # type: ignore[assignment]
                        if current is None:
                            break
                        cycle.append(current)
                    cycle.reverse()
                    cycle.append(cycle[0])  # Close the cycle
                    return cycle

                if state[neighbor] == 0:
                    parent[neighbor] = node
                    stack.append((neighbor, 0))
            else:
                state[node] = 2  # Done

    return None


# Regex for State Delta section headers like:
# ### ✅ PP02_checkout_redesign — Sep 2025
# ### 🔄 SP01_dream_v405_implementation — Feb 2026
_STATE_DELTA_HEADER_RE = re.compile(
    r"^###\s+.*?(\w+\d+\S*)\s*[—–-]\s*(.+)$"
)

# Regex for State Delta bullet entries like:
# - dream_mcp: skeleton not yet created (p03 pending)
# - checkout: linear flow → reservation-based state machine
# - ⏳ dream_mcp: skeleton not yet created (emoji prefix variant)
# - `_templates/`: renamed from ... (backtick-wrapped variant)
_STATE_DELTA_ENTRY_RE = re.compile(
    r"^-\s+(?:[^\w`]*)?`?(\w[\w./-]*)`?:\s+(.+)$"
)


def _parse_state_deltas_for_module(
    file_path: Path,
    module_name: str,
) -> list[dict[str, str]]:
    """Parse a markdown file for State Delta entries referencing a module.

    Scans for State Delta sections (``### [emoji] PlanName — Date``)
    and collects bullet entries (``- module_name: description``) that
    match the target module.

    Args:
        file_path: Path to the markdown file to scan.
        module_name: Module name to filter for.

    Returns:
        List of dicts with ``date``, ``plan``, ``change`` keys.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError:
        _logger.debug(f"Could not read {file_path} for State Delta parsing")
        return []

    entries: list[dict[str, str]] = []
    current_plan: str | None = None
    current_date: str | None = None
    in_state_deltas = False

    for line in content.splitlines():
        stripped = line.strip()

        # Detect State Deltas section
        if stripped.startswith("## State Deltas"):
            in_state_deltas = True
            continue

        # Detect leaving State Deltas section (hit another ## heading)
        if in_state_deltas and stripped.startswith("## ") and "State Deltas" not in stripped:
            in_state_deltas = False
            continue

        if not in_state_deltas:
            continue

        # Match section headers
        header_match = _STATE_DELTA_HEADER_RE.match(stripped)
        if header_match:
            current_plan = header_match.group(1)
            current_date = header_match.group(2).strip()
            continue

        # Match bullet entries
        entry_match = _STATE_DELTA_ENTRY_RE.match(stripped)
        if entry_match and current_plan is not None:
            entry_module = entry_match.group(1)
            entry_desc = entry_match.group(2)

            # Match module name (exact or prefix for qualified names)
            if entry_module == module_name or module_name in entry_module:
                entries.append({
                    "date": current_date or "unknown",
                    "plan": current_plan,
                    "change": entry_desc,
                })

    return entries


def _update_frontmatter_field(
    content: str,
    field: str,
    value: str,
) -> str:
    """Update or insert a YAML frontmatter field in markdown content.

    If the field exists in the frontmatter, its value is replaced.
    If the field does not exist, it is appended before the closing ``---``.

    Args:
        content: Full markdown file content.
        field: YAML field name to update.
        value: New value for the field.

    Returns:
        Updated content string.
    """
    # Find the frontmatter boundaries
    lines = content.split("\n")

    # Find opening and closing ---
    fm_start: int | None = None
    fm_end: int | None = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "---":
            if fm_start is None:
                fm_start = i
            else:
                fm_end = i
                break

    if fm_start is None or fm_end is None:
        return content

    # Check if field already exists in frontmatter
    field_pattern = re.compile(rf"^{re.escape(field)}\s*:")
    field_found = False

    for i in range(fm_start + 1, fm_end):
        if field_pattern.match(lines[i]):
            lines[i] = f"{field}: {value}"
            field_found = True
            break

    if not field_found:
        # Insert before closing ---
        lines.insert(fm_end, f"{field}: {value}")

    return "\n".join(lines)


def _current_quarter_dirname() -> str:
    """Generate the current quarter directory name (``YYYY-QN``).

    Returns:
        String like ``"2026-Q1"`` based on current date.
    """
    today = date.today()
    quarter = math.ceil(today.month / 3)
    return f"{today.year}-Q{quarter}"
