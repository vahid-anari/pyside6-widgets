# pyside6-widgets

[![PyPI version](https://badge.fury.io/py/pyside6-widgets.svg)](https://pypi.org/project/pyside6-widgets/)

Reusable PySide6 GUI components for scientific applications.

Built from real scientific software, these widgets are production-tested and
designed to be dropped into any PySide6 project with no external dependencies
beyond PySide6 itself (plus Matplotlib for the SVG label).

## Components

| Widget / Module | Description |
|-----------------|-------------|
| `MathLabel` | SVG-backed label with optional LaTeX rendering via Matplotlib |
| `NumericLineEdit` | Validated numeric input with scientific notation and range checking |
| `SciNumberValidator` | Qt validator for integer and float input |
| `MenuBarController` | Build a full Qt menu bar from a Python dict — no boilerplate |
| `StatusBarController` | State-aware status bar with live memory and elapsed-time display |
| `dialogs` | General-purpose message, info, about, and confirmation dialogs |

## Installation

```bash
pip install pyside6-widgets
```

## Quick Start

### MathLabel

Renders math expressions using Matplotlib's mathtext engine.
Pass `use_tex=True` only if a LaTeX distribution is installed on the system.

```python
from pyside6_widgets import MathLabel

# Matplotlib mathtext (no LaTeX installation needed)
label = MathLabel(text=r"E=mc^2", font_size=20, text_color="black")

# Full LaTeX rendering (requires LaTeX installation)
label = MathLabel(text=r"E=mc^2", font_size=20, use_tex=True)
```

### NumericLineEdit

```python
from pyside6_widgets import NumericLineEdit

# Float input in range [0, 100]
edit = NumericLineEdit(init_val=1.5, min_limit=0.0, max_limit=100.0, val_fmt="{:.3g}")
edit.valueChanged.connect(lambda v: print(f"New value: {v}"))

# Integer input
edit = NumericLineEdit(init_val=10, value_is_int=True, min_limit=0, max_limit=999)
```

### MenuBarController

```python
from PySide6.QtWidgets import QMainWindow
from pyside6_widgets import MenuBarController

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        menu_spec = {
            "File": [
                {"id": "open", "text": "Open…", "shortcut": "Ctrl+O"},
                {"id": "sep"},
                {"id": "quit", "text": "Quit", "shortcut": "Ctrl+Q"},
            ],
            "View": [
                {"id": "dark_mode", "text": "Dark Mode", "checkable": True},
            ],
        }
        self.menu = MenuBarController(self, menu_spec=menu_spec)
        self.menu.actionTriggered.connect(self.on_action)

    def on_action(self, menu: str, action_id: str, checked: bool):
        print(f"{menu} → {action_id} (checked={checked})")
```

### StatusBarController

```python
from PySide6.QtWidgets import QMainWindow
from pyside6_widgets import StatusBarController, StatusState

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.status = StatusBarController(self)

    def run_solver(self):
        self.status.set_state(StatusState.SOLVING)   # starts timer
        # ... do work ...
        self.status.set_state(StatusState.READY)     # stops timer
```

### Dialogs

```python
from pyside6_widgets import (
    show_information, show_warning, show_critical,
    show_about_dialog, ask_question, AskResult,
)

# Simple message dialogs
show_information("Done", "The export completed successfully.")
show_warning("Warning", "File already exists.")
show_critical("Error", "Could not open file.")

# About dialog
show_about_dialog(
    title="My App",
    html_text="<p>Version 1.0</p><p>Author: Vahid Anari</p>",
    heading="My App",
)

# Confirmation dialog
result = ask_question("Confirm", "Are you sure you want to delete this?")
if result == AskResult.YES:
    delete()
```

## Requirements

- Python 3.10+
- PySide6 >= 6.5
- matplotlib >= 3.7 *(required only for `MathLabel`)*
- psutil >= 5.9 *(required only for `StatusBarController`)*

## License

MIT License — see [LICENSE](LICENSE) for details.

## Author

Vahid Anari —
[GitHub](https://github.com/vahid-anari) ·
[LinkedIn](https://www.linkedin.com/in/vahid-anari/)

Reusable PySide6 GUI components — validated numeric inputs, math labels, declarative menu bar, status bar, and dialogs.
