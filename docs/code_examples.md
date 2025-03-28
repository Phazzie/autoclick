# Code Examples

This document contains code examples for the advanced features implementation.

## Core Components

### 1. Condition System

```python
# src/core/conditions/condition_interface.py
from abc import ABC, abstractmethod
from typing import Any, Dict

class ConditionInterface(ABC):
    @abstractmethod
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate the condition with the given context"""
        pass
```

```python
# src/core/conditions/element_exists_condition.py
from typing import Any, Dict
from src.core.conditions.condition_interface import ConditionInterface

class ElementExistsCondition(ConditionInterface):
    def __init__(self, selector: str):
        self.selector = selector

    def evaluate(self, context: Dict[str, Any]) -> bool:
        driver = context.get("driver")
        if not driver:
            return False

        try:
            element = driver.find_element_by_css_selector(self.selector)
            return element is not None
        except:
            return False
```

### 2. Loop System

```python
# src/core/loops/loop_interface.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator

class LoopInterface(ABC):
    @abstractmethod
    def initialize(self, context: Dict[str, Any]) -> None:
        """Initialize the loop with the given context"""
        pass

    @abstractmethod
    def has_next(self, context: Dict[str, Any]) -> bool:
        """Check if there are more iterations"""
        pass

    @abstractmethod
    def next(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Move to the next iteration and update context"""
        pass
```

```python
# src/core/loops/count_loop.py
from typing import Any, Dict
from src.core.loops.loop_interface import LoopInterface

class CountLoop(LoopInterface):
    def __init__(self, count: int, variable_name: str = "index"):
        self.count = count
        self.variable_name = variable_name
        self.current = 0

    def initialize(self, context: Dict[str, Any]) -> None:
        self.current = 0
        context["variables"][self.variable_name] = self.current

    def has_next(self, context: Dict[str, Any]) -> bool:
        return self.current < self.count

    def next(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.current += 1
        context["variables"][self.variable_name] = self.current
        return context
```

### 3. Variable System

```python
# src/core/variables/variable_storage.py
from typing import Any, Dict, Optional

class VariableStorage:
    def __init__(self):
        self.global_variables: Dict[str, Any] = {}
        self.workflow_variables: Dict[str, Any] = {}
        self.local_variables: Dict[str, Any] = {}

    def get(self, name: str) -> Optional[Any]:
        # Check local first, then workflow, then global
        if name in self.local_variables:
            return self.local_variables[name]
        if name in self.workflow_variables:
            return self.workflow_variables[name]
        if name in self.global_variables:
            return self.global_variables[name]
        return None

    def set(self, name: str, value: Any, scope: str = "workflow") -> None:
        if scope == "global":
            self.global_variables[name] = value
        elif scope == "workflow":
            self.workflow_variables[name] = value
        elif scope == "local":
            self.local_variables[name] = value

    def clear_local(self) -> None:
        self.local_variables.clear()

    def clear_workflow(self) -> None:
        self.workflow_variables.clear()

    def clear_all(self) -> None:
        self.global_variables.clear()
        self.workflow_variables.clear()
        self.local_variables.clear()
```

### 4. Data Source System

```python
# src/core/data/data_source_interface.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator, List

class DataSourceInterface(ABC):
    @abstractmethod
    def get_columns(self) -> List[str]:
        """Get the column names"""
        pass

    @abstractmethod
    def get_row_count(self) -> int:
        """Get the number of rows"""
        pass

    @abstractmethod
    def get_rows(self) -> Iterator[Dict[str, Any]]:
        """Get an iterator over all rows"""
        pass
```

```python
# src/core/data/csv_data_source.py
import csv
from typing import Any, Dict, Iterator, List
from src.core.data.data_source_interface import DataSourceInterface

class CsvDataSource(DataSourceInterface):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._columns: List[str] = []
        self._row_count = 0
        self._initialize()

    def _initialize(self) -> None:
        with open(self.file_path, 'r', newline='') as f:
            reader = csv.reader(f)
            self._columns = next(reader)  # First row is headers
            rows = list(reader)
            self._row_count = len(rows)

    def get_columns(self) -> List[str]:
        return self._columns.copy()

    def get_row_count(self) -> int:
        return self._row_count

    def get_rows(self) -> Iterator[Dict[str, Any]]:
        with open(self.file_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield dict(row)
```

### 5. Error Handling System

```python
# src/core/errors/error_types.py
from enum import Enum, auto
from datetime import datetime
from typing import Dict, Any

class ErrorType(Enum):
    ELEMENT_NOT_FOUND = auto()
    TIMEOUT = auto()
    NAVIGATION_ERROR = auto()
    JAVASCRIPT_ERROR = auto()
    AUTHENTICATION_ERROR = auto()
    NETWORK_ERROR = auto()
    UNKNOWN = auto()

class Error:
    def __init__(self, type: ErrorType, message: str, details: Dict[str, Any] = None):
        self.type = type
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now()
```

```python
# src/core/errors/recovery_strategy_interface.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from src.core.errors.error_types import Error

class RecoveryStrategyInterface(ABC):
    @abstractmethod
    def can_recover(self, error: Error) -> bool:
        """Check if this strategy can recover from the given error"""
        pass

    @abstractmethod
    def recover(self, error: Error, context: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to recover from the error"""
        pass
```

### 6. Reporting System

```python
# src/core/reporting/report_interface.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class ReportInterface(ABC):
    @abstractmethod
    def generate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a report from the given data"""
        pass

    @abstractmethod
    def export(self, format: str, path: Optional[str] = None) -> str:
        """Export the report in the specified format"""
        pass
```

## UI Components

### 1. Condition Editor

```python
# src/ui/components/condition_editor.py
import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Dict, Optional

from src.ui.components.base_component import BaseComponent

class ConditionEditor(BaseComponent):
    def __init__(self, parent: Any, on_save: Callable[[Dict[str, Any]], None]):
        super().__init__(parent)
        self.on_save = on_save
        self._create_ui()

    # UI implementation details...
```

### 2. Loop Editor

```python
# src/ui/components/loop_editor.py
import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Dict, Optional

from src.ui.components.base_component import BaseComponent

class LoopEditor(BaseComponent):
    def __init__(self, parent: Any, on_save: Callable[[Dict[str, Any]], None]):
        super().__init__(parent)
        self.on_save = on_save
        self._create_ui()

    # UI implementation details...
```

### 3. Variable Manager

```python
# src/ui/components/variable_manager.py
import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, List, Optional

from src.ui.components.base_component import BaseComponent

class VariableManager(BaseComponent):
    def __init__(self, parent: Any, variable_storage):
        super().__init__(parent)
        self.variable_storage = variable_storage
        self._create_ui()

    # UI implementation details...
```

## Testing Examples

### Unit Tests

```python
# tests/core/conditions/test_element_exists_condition.py
import unittest
from unittest.mock import MagicMock
from src.core.conditions.element_exists_condition import ElementExistsCondition

class TestElementExistsCondition(unittest.TestCase):
    def test_element_exists(self):
        # Arrange
        driver = MagicMock()
        element = MagicMock()
        driver.find_element_by_css_selector.return_value = element
        context = {"driver": driver}
        condition = ElementExistsCondition("#test-element")

        # Act
        result = condition.evaluate(context)

        # Assert
        self.assertTrue(result)
        driver.find_element_by_css_selector.assert_called_once_with("#test-element")

    def test_element_does_not_exist(self):
        # Arrange
        driver = MagicMock()
        driver.find_element_by_css_selector.side_effect = Exception("Element not found")
        context = {"driver": driver}
        condition = ElementExistsCondition("#test-element")

        # Act
        result = condition.evaluate(context)

        # Assert
        self.assertFalse(result)
        driver.find_element_by_css_selector.assert_called_once_with("#test-element")
```

### Integration Tests

```python
# tests/integration/test_conditional_workflow.py
import unittest
from unittest.mock import MagicMock
from src.core.conditions.element_exists_condition import ElementExistsCondition
from src.core.actions.if_then_else_action import IfThenElseAction
from src.core.actions.click_action import ClickAction
from src.core.workflow.workflow_engine import WorkflowEngine

class TestConditionalWorkflow(unittest.TestCase):
    def test_if_then_else_workflow(self):
        # Arrange
        driver = MagicMock()
        element = MagicMock()
        driver.find_element_by_css_selector.return_value = element

        context = {
            "driver": driver,
            "variables": MagicMock()
        }

        # Create actions
        condition = ElementExistsCondition("#test-button")
        then_action = ClickAction("#test-button")
        else_action = ClickAction("#alternative-button")

        if_action = IfThenElseAction(condition, then_action, else_action)

        # Create workflow engine
        engine = WorkflowEngine()

        # Act
        result = engine.execute_action(if_action, context)

        # Assert
        self.assertTrue(result["success"])
        element.click.assert_called_once()
```

### End-to-End Tests

```python
# tests/e2e/test_data_driven_workflow.py
import os
import unittest
import tempfile
import csv
from unittest.mock import MagicMock
from src.core.data.csv_data_source import CsvDataSource
from src.core.actions.navigate_action import NavigateAction
from src.core.actions.input_action import InputAction
from src.core.actions.click_action import ClickAction
from src.core.workflow.data_driven_workflow import DataDrivenWorkflow

class TestDataDrivenWorkflow(unittest.TestCase):
    def setUp(self):
        # Create a temporary CSV file with test data
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = os.path.join(self.temp_dir.name, "test_data.csv")

        with open(self.csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password"])
            writer.writerow(["user1", "pass1"])
            writer.writerow(["user2", "pass2"])

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_login_workflow(self):
        # Arrange
        data_source = CsvDataSource(self.csv_path)

        # Create actions for a login workflow
        actions = [
            NavigateAction("https://example.com/login"),
            InputAction("#username", "${username}"),
            InputAction("#password", "${password}"),
            ClickAction("#login-button")
        ]

        # Create variable mappings
        variable_mappings = {
            "username": "username",
            "password": "password"
        }

        # Create data-driven workflow
        workflow = DataDrivenWorkflow(data_source, actions, variable_mappings)

        # Create a mock context with a driver
        driver = MagicMock()
        context = {
            "driver": driver,
            "variables": MagicMock()
        }

        # Act
        results = workflow.execute(context)

        # Assert
        self.assertEqual(len(results), 2)  # Two rows in the CSV
        self.assertTrue(results[0]["success"])
        self.assertTrue(results[1]["success"])
```
