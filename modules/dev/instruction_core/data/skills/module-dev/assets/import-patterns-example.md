# Import Patterns — Correct vs Wrong

## ✅ Correct: package imports via uv editable installs

```python
from logger_util import Logger
from config_manager import ConfigManager
from exceptions_core import ADHDError
```

## ❌ Wrong: sys.path manipulation

```python
import sys
sys.path.insert(0, "../../foundation/logger_util")
```

## ❌ Wrong: relative imports across module boundaries

```python
from ..foundation.logger_util import Logger
```
