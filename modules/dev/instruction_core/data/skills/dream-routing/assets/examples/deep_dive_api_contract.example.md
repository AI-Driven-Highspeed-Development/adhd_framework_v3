<!-- ═══════════════════════════════════════════════════════════════════
     ADHD-MANAGED — DO NOT EDIT DIRECTLY
     Source: modules/dev/instruction_core/data/.agent_plan/day_dream/_templates/examples/deep_dive_api_contract.example.md
     Refresh: adhd r -f
═══════════════════════════════════════════════════════════════════ -->

## 🔬 Deep Dive

### API Contract: Plugin Registration System

**Context:** Defining the public contract for a plugin/extension registry that allows third-party modules to register capabilities at runtime. This pattern applies to CLI tools, web frameworks, or any extensible system.

---

### 1. Core Interface Definition

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable
from dataclasses import dataclass

T = TypeVar("T")

class Plugin(ABC):
    """Base class all plugins must inherit from."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for this plugin (e.g., 'csv-exporter')."""
        ...
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Semantic version (e.g., '1.2.0')."""
        ...
    
    @property
    def dependencies(self) -> list[str]:
        """Other plugin names this depends on. Default: none."""
        return []
    
    def on_load(self) -> None:
        """Called when plugin is registered. Override for setup."""
        pass
    
    def on_unload(self) -> None:
        """Called when plugin is unregistered. Override for cleanup."""
        pass
```

---

### 2. Registry Contract

```python
@dataclass(frozen=True)
class PluginInfo:
    """Metadata returned by registry queries."""
    name: str
    version: str
    dependencies: list[str]
    load_order: int          # 0 = first loaded
    is_active: bool
    error: str | None        # Populated if load failed


class PluginRegistry:
    """Central registry for plugin lifecycle management."""
    
    def register(
        self,
        plugin: Plugin,
        *,
        replace: bool = False,    # Replace if already registered
        auto_load: bool = True,   # Call on_load() immediately
    ) -> PluginInfo:
        """
        Register a plugin with the system.
        
        Raises:
            DuplicatePluginError: Plugin with same name exists (and replace=False)
            DependencyError: Required dependency not registered
            PluginLoadError: on_load() raised an exception
        """
    
    def unregister(self, name: str) -> bool:
        """
        Remove a plugin. Calls on_unload() before removal.
        
        Returns:
            True if plugin was found and removed, False if not found.
        
        Raises:
            DependencyError: Other plugins depend on this one.
        """
    
    def get(self, name: str) -> Plugin | None:
        """Get plugin instance by name. Returns None if not found."""
    
    def list_plugins(
        self,
        *,
        active_only: bool = True,
    ) -> list[PluginInfo]:
        """List all registered plugins, optionally filtering by state."""
    
    def is_registered(self, name: str) -> bool:
        """Check if a plugin is registered."""
```

---

### 3. Event Hooks (Optional Extension)

For plugins that need to respond to system events:

```python
from enum import Enum, auto

class LifecycleEvent(Enum):
    APP_STARTING = auto()
    APP_READY = auto()
    APP_SHUTTING_DOWN = auto()
    CONFIG_RELOADED = auto()

class EventAwarePlugin(Plugin):
    """Plugin that can subscribe to lifecycle events."""
    
    def on_event(self, event: LifecycleEvent, context: dict) -> None:
        """Override to handle specific events."""
        pass
    
    @property
    def subscribed_events(self) -> list[LifecycleEvent]:
        """Events this plugin wants to receive. Default: all."""
        return list(LifecycleEvent)
```

---

### 4. Error Hierarchy

```python
class PluginError(Exception):
    """Base exception for all plugin-related errors."""
    pass

class DuplicatePluginError(PluginError):
    """Raised when registering a plugin that already exists."""
    def __init__(self, name: str, existing_version: str):
        self.name = name
        self.existing_version = existing_version
        super().__init__(f"Plugin '{name}' v{existing_version} already registered")

class DependencyError(PluginError):
    """Raised when dependencies are missing or would break."""
    def __init__(self, plugin: str, missing: list[str]):
        self.plugin = plugin
        self.missing = missing
        super().__init__(f"Plugin '{plugin}' requires: {', '.join(missing)}")

class PluginLoadError(PluginError):
    """Raised when on_load() fails."""
    def __init__(self, name: str, cause: Exception):
        self.name = name
        self.cause = cause
        super().__init__(f"Plugin '{name}' failed to load: {cause}")
```

---

### 5. Usage Example

```python
# Defining a plugin
class MarkdownExporter(Plugin):
    @property
    def name(self) -> str:
        return "markdown-exporter"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def dependencies(self) -> list[str]:
        return ["core-formatter"]  # Requires this plugin first
    
    def on_load(self) -> None:
        print(f"{self.name} loaded!")
    
    def export(self, content: str) -> str:
        return f"# Export\n\n{content}"

# Using the registry
registry = PluginRegistry()

# Register dependency first
registry.register(CoreFormatter())

# Then register dependent plugin
info = registry.register(MarkdownExporter())
print(f"Registered: {info.name} v{info.version}")

# Use the plugin
exporter = registry.get("markdown-exporter")
if exporter:
    result = exporter.export("Hello world")
```

---

### 6. Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Registration: push vs pull | Push (explicit register) | Simpler, no magic discovery |
| Dependencies: strict or lazy | Strict (fail fast) | Prevents runtime surprises |
| Versioning: semantic or date | Semantic | Industry standard |
| Multiple versions | No (one active) | Complexity not worth it P0 |
| Thread-safety | Lock on register/unregister | Reads are lock-free after startup |

---

### 7. Anti-Patterns to Avoid

| ❌ Don't | ✅ Do Instead | Why |
|----------|---------------|-----|
| Auto-discover plugins via `__subclasses__` | Explicit registration | Predictable, testable |
| Allow circular dependencies | Fail at registration | Prevents deadlocks |
| Let plugins modify other plugins | Event system for communication | Loose coupling |
| Global singleton registry | Injectable registry instance | Testable, multiple contexts |
| Silent failures on load | Raise or log + mark inactive | Don't hide problems |
