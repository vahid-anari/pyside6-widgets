"""pyside6-widgets — Reusable PySide6 GUI components.

Modules
-------
dialogs
    General-purpose message, information, about, and confirmation dialogs.
labels
    SVG-backed label with optional LaTeX rendering via Matplotlib.
numeric_line_edit
    Validated numeric line-edit with scientific notation and range checking.
menu_bar_controller
    Declarative menu-bar builder from a Python dict specification.
status_bar_controller
    State-aware status bar with live memory and elapsed-time display.
"""

from .dialogs import (
    AskResult,
    DialogIcon,
    TitledDialogBase,
    MessageDialog,
    InfoDialog,
    AboutDialog,
    AskDialog,
    show_information,
    show_rich_information,
    show_about_dialog,
    show_warning,
    show_critical,
    ask_question,
)
from .labels import MathLabel
from .numeric_line_edit import NumericLineEdit, SciNumberValidator
from .menu_bar_controller import MenuBarController
from .status_bar_controller import StatusBarController, StatusState

__all__ = [
    # dialogs
    "AskResult",
    "DialogIcon",
    "TitledDialogBase",
    "MessageDialog",
    "InfoDialog",
    "AboutDialog",
    "AskDialog",
    "show_information",
    "show_rich_information",
    "show_about_dialog",
    "show_warning",
    "show_critical",
    "ask_question",
    # labels
    "MathLabel",
    # numeric_line_edit
    "NumericLineEdit",
    "SciNumberValidator",
    # menu_bar_controller
    "MenuBarController",
    # status_bar_controller
    "StatusBarController",
    "StatusState",
]

__version__ = "0.1.0"
__author__ = "Vahid Anari"
__email__ = "vahid.anari8@gmail.com"
