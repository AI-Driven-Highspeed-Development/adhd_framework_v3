---
applyTo: "modules/**/init.yaml"
---

> **⚠️ DEPRECATION NOTICE**: `init.yaml` is being phased out in P3 (Phase 3) in favor of `pyproject.toml` metadata.
> New modules should NOT create init.yaml files. Existing modules will be migrated.
> This documentation is retained for legacy module maintenance only.

# Module init.yaml Authoring Instructions

`init.yaml`: Metadata:
- version: str (e.g., 0.0.1)
- folder_path: str (e.g., modules/runtime/config_manager) # legacy, do not use or remove.
- layer: str (foundation | runtime | dev)
- repo_url: str (url to module repo in GitHub)
- shows_in_workspace: bool (whether to show in ADHD workspace UI)
- requirements: list of str (urls of required ADHD modules)

## Instructions for Creating/Editing `init.yaml` Files

1. **Versioning**: Follow semantic versioning (MAJOR.MINOR.PATCH). Increment:
   - MAJOR for incompatible changes,
   - MINOR features,
   - PATCH for bug fixes.
   - Start at 0.0.1 for new modules.
   - No need to update version unless user explicitly requests.

2. **Folder Path**: Specify the module's folder path relative to the project root (e.g., `managers/config_manager`). This is for legacy purposes; new modules should not have this field, old modules should retain it, only user can manually remove it.

3. **Layer**: Choose from predefined layers:
   - `foundation` (bootstrap-time, no ADHD deps), `runtime` (most modules), `dev` (development tools).

4. **Requirements**: List of URLs to required ADHD modules (e.g., `https://github.com/AI-Driven-Highspeed-Development/exceptions_core.git`).

5. **Testing Scope** (Optional): Define constraints for HyperRed adversarial testing:
   ```yaml
   testing:
     has_tests: true  # Whether module has tests/ folder (default: false)
     scope:
       platforms:
         - linux
         - macos
       python_versions:
         - "3.10"
         - "3.11"
       threat_model: internal  # internal | external | adversarial
       input_assumptions:
         - "Inputs are from trusted internal sources"
       out_of_scope:
         - "Cross-platform compatibility"
         - "Performance under extreme load"
   ```
   
   **Threat Model Levels**:
   - `internal`: Inputs from trusted sources (other modules, config files). Test for programmer mistakes.
   - `external`: Inputs from untrusted users (CLI, API). Test for accidental bad input.
   - `adversarial`: Inputs from attackers. Full fuzzing and injection testing.
   
   **Default**: If omitted, HyperRed assumes `platforms: [linux, macos]`, `threat_model: internal`.