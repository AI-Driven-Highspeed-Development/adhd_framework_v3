<!-- GENERATED — run 'dream tree' to refresh -->
<!-- Generated: 2026-03-02T04:48:34Z -->

# Day Dream — Plan Tree

```
.agent_plan/day_dream/
├── _overview.md
├── _tree.md
├── DREAM_v4.05.md
├── _archive/
│   ├── README.md
│   ├── dream-upgrade/
│   │   ├── _overview.md
│   │   ├── architecture.md
│   │   ├── executive-summary.md
│   │   ├── implementation.md
│   │   ├── module-structure.md
│   │   ├── p1-non-vibe-code.md
│   │   ├── plan.yaml
│   │   ├── p0-fix-blueprint-system/
│   │   │   ├── _overview.md
│   │   │   ├── fix-backward-compat.md
│   │   │   ├── fix-estimation.md
│   │   │   └── fix-walking-skeleton.md
│   │   └── p2-dream-integration/
│   │       ├── _overview.md
│   │       ├── dream-planning-skill.md
│   │       ├── template-refresh.md
│   │       └── update-day-dream-skill.md
│   └── dream_iterations/
│       ├── DREAM_v3.md
│       ├── DREAM_v4.01.md
│       ├── DREAM_v4.02.md
│       ├── DREAM_v4.02_concept_demo.md
│       ├── DREAM_v4.02_concept_report.md
│       ├── DREAM_v4.03.md
│       ├── DREAM_v4.03_stress_test_demo.md
│       ├── DREAM_v4.03_stress_test_report.md
│       ├── DREAM_v4.04.md
│       ├── DREAM_v4.04_stress_test_demo.md
│       ├── DREAM_v4.04_stress_test_report.md
│       └── DREAM_v4.md
├── _templates/
│   ├── README.md
│   ├── simple.template.md
│   ├── assets/
│   │   └── asset.template.md
│   ├── blueprint/
│   │   ├── 00_index.template.md
│   │   ├── 01_executive_summary.template.md
│   │   ├── 01_summary.template.md
│   │   ├── 02_architecture.template.md
│   │   ├── 80_implementation.template.md
│   │   ├── 81_module_structure.template.md
│   │   ├── 82_cli_commands.template.md
│   │   ├── 99_references.template.md
│   │   ├── deep_dive_reference.md
│   │   ├── exploration.template.md
│   │   ├── NN_feature.template.md
│   │   ├── NN_feature_simple.template.md
│   │   ├── overview.template.md
│   │   ├── task.template.md
│   │   └── modules/
│   │       └── module_spec.template.md
│   └── examples/
│       ├── deep_dive_algorithm_proof.example.md
│       ├── deep_dive_api_contract.example.md
│       ├── deep_dive_architecture.example.md
│       ├── deep_dive_state_machine.example.md
│       ├── free_zone_assumption_graveyard.example.md
│       ├── free_zone_metaphor_map.example.md
│       ├── free_zone_philosophical_tensions.example.md
│       ├── simple_example.md
│       └── blueprint_example/
│           ├── 00_index.md
│           └── 01_executive_summary.md
├── blueprint/
│   ├── 00_index.md
│   ├── 01_executive_summary.md
│   ├── 02_architecture.md
│   ├── 03_feature_fix_estimation.md
│   ├── 04_feature_fix_walking_skeleton.md
│   ├── 05_feature_fix_backward_compat.md
│   ├── 06_feature_dream_planning_skill.md
│   ├── 07_feature_update_day_dream_skill.md
│   ├── 08_feature_template_refresh.md
│   ├── 09_feature_non_vibe_code.md
│   ├── 80_implementation.md
│   └── 81_module_structure.md
├── module-lifecycle/
│   ├── _overview.md
│   ├── architecture.md
│   ├── cli_commands.md
│   ├── executive_summary.md
│   ├── implementation.md
│   ├── module_structure.md
│   ├── plan.yaml
│   ├── p00_prerequisites/
│   │   ├── 01_pyproject_patcher_remove.md
│   │   ├── 02_reverse_dep_lookup.md
│   │   └── _overview.md
│   ├── p01_core_commands/
│   │   ├── 01_remove_command.md
│   │   ├── 02_safety_features.md
│   │   ├── 03_update_command.md
│   │   └── _overview.md
│   └── p02_batch_operations/
│       ├── 01_batch_update_command.md
│       └── _overview.md
├── PP02_context_injection_restructure/  ✅ [DONE]
│   ├── 01_summary.md
│   ├── 80_implementation.md
│   ├── _overview.md
│   └── p00_usage_audit/
│       └── 01_usage_audit_matrix.md
├── PP03_dream_sop_skills/  ✅ [DONE]
│   ├── 01_summary.md
│   ├── 80_implementation.md
│   └── _overview.md
└── SP01_dream_v405_implementation/  🔄 [WIP]
    ├── 01_executive_summary.md
    ├── 02_architecture.md
    ├── 80_implementation.md
    ├── 81_module_structure.md
    ├── _overview.md
    ├── modules/
    │   ├── dream_mcp.md
    │   └── instruction_core.md
    ├── p00_foundation/  ✅ [DONE]
    │   ├── 01_rename_templates_dir.md
    │   ├── 02_create_pp_summary_template.md
    │   ├── 03_update_template_schema.md
    │   └── _overview.md
    ├── p01_skill_updates/  ✅ [DONE]
    │   ├── 01_update_dream_planning_skill.md
    │   ├── 02_update_day_dream_skill.md
    │   ├── 03_update_writing_templates_skill.md
    │   └── _overview.md
    ├── p02_agent_instruction_updates/  ✅ [DONE]
    │   ├── 01_update_flow_sources_and_agents.md
    │   ├── 02_update_remaining_path_references.md
    │   └── _overview.md
    ├── p03_dream_mcp_skeleton/  ✅ [DONE]
    │   ├── 01_create_module_skeleton.md
    │   └── _overview.md
    ├── p04_parsing_and_simple_commands/  ⏳ [TODO]
    │   ├── 01_shared_parsing_infrastructure.md
    │   ├── 02_dream_tree_command.md
    │   ├── 03_dream_stale_command.md
    │   └── _overview.md
    ├── p05_status_and_validate/  ⏳ [TODO]
    │   ├── 01_dream_status_command.md
    │   ├── 02_dream_validate_core.md
    │   ├── 03_dream_validate_dag.md
    │   └── _overview.md
    ├── p06_advanced_workflows/  ⏳ [TODO]
    │   ├── 01_dream_impact_command.md
    │   ├── 02_dream_history_command.md
    │   ├── 03_dream_emergency_archive.md
    │   └── _overview.md
    └── p07_intelligence_layer/  ⏳ [TODO]
        ├── 01_dream_hypothetical_impact.md
        ├── 02_dream_proactive_gaps.md
        └── _overview.md
```
