"""Reusable dialog widgets for PySide6 applications.

Provides simple message, information, about, and confirmation dialogs
with no external dependencies beyond PySide6.
"""

from __future__ import annotations

import html
from enum import Enum, auto
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication, QTextCursor
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QStyle,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


class AskResult(Enum):
    """Possible outcomes of a question dialog."""

    YES = auto()
    NO = auto()
    CANCEL = auto()


class DialogIcon(Enum):
    """Supported standard-icon presets for reusable dialogs."""

    INFORMATION = QStyle.SP_MessageBoxInformation
    WARNING = QStyle.SP_MessageBoxWarning
    CRITICAL = QStyle.SP_MessageBoxCritical
    QUESTION = QStyle.SP_MessageBoxQuestion


def _make_html_label(html_text: str) -> QLabel:
    """Create a rich-text label with selection and external-link support.

    Args:
        html_text: HTML text to display.

    Returns:
        Configured rich-text label.
    """
    label = QLabel(html_text)
    label.setTextFormat(Qt.RichText)
    label.setOpenExternalLinks(True)
    label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
    label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    return label


def _try_load_app_icon_pixmap(size: int, icon_path: Optional[str] = None) -> Optional[QPixmap]:
    """Return the application icon pixmap when the icon file can be loaded.

    Args:
        size: Requested icon size in pixels.
        icon_path: Optional path to the icon file. If ``None`` or the file
            does not exist, returns ``None``.

    Returns:
        Scaled pixmap if the icon file exists and loads successfully, otherwise
        ``None``.
    """
    if icon_path is None:
        return None

    path = Path(icon_path)
    if not path.exists():
        return None

    pixmap = QPixmap(str(path))
    if pixmap.isNull():
        return None

    return pixmap.scaled(
        size,
        size,
        Qt.KeepAspectRatio,
        Qt.SmoothTransformation,
    )


class TitledDialogBase(QDialog):
    """Common dialog base class with title text, optional icon, and body helpers."""

    def __init__(
            self,
            title: str,
            text: str,
            informative_text: str = "",
            icon: Optional[DialogIcon] = None,
            parent: Optional[QWidget] = None,
    ) -> None:
        """Initialize the common titled-dialog layout.

        Args:
            title: Window title.
            text: Main dialog text.
            informative_text: Optional secondary explanatory text.
            icon: Optional standard dialog icon preset.
            parent: Optional parent widget.
        """
        super().__init__(parent)

        left_margin = 5
        icon_margin = 10
        right_margin = 8
        top_margin = 0
        bottom_margin = 7

        self.setWindowTitle(title)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(6)

        text_label = _make_html_label(text.replace("\n", "<br>"))
        text_layout.addWidget(text_label)

        if informative_text:
            info_label = _make_html_label(informative_text.replace("\n", "<br>"))
            text_layout.addWidget(info_label)

        row = QHBoxLayout()
        row.addSpacing(left_margin)
        if icon is not None:
            std_icon = self.style().standardIcon(icon.value)
            pixmap = std_icon.pixmap(32, 32)
            icon_label = QLabel()
            icon_label.setPixmap(pixmap)
            icon_label.setFixedSize(icon_label.sizeHint())
            row.addWidget(icon_label, alignment=Qt.AlignTop)
            row.addSpacing(icon_margin)
        row.addLayout(text_layout)
        row.addSpacing(right_margin)

        self._layout = QVBoxLayout(self)
        self._layout.addSpacing(top_margin)
        self._layout.addLayout(row)
        self._layout.addSpacing(bottom_margin)
        self._layout.addStretch(1)

    def add_layout(self, layout: QLayout) -> None:
        """Add a layout to the dialog body.

        Args:
            layout: Layout to append to the main dialog layout.
        """
        self._layout.addLayout(layout)

    def add_widget(self, widget: QWidget) -> None:
        """Add a widget to the dialog body.

        Args:
            widget: Widget to append to the main dialog layout.
        """
        self._layout.addWidget(widget)

    def add_stretch(self, stretch: int = 1) -> None:
        """Add stretch space to the dialog body.

        Args:
            stretch: Stretch factor to add.
        """
        self._layout.addStretch(stretch)


class MessageDialog(TitledDialogBase):
    """Simple informational dialog with a single acknowledgement button."""

    def __init__(
            self,
            title: str,
            text: str,
            informative_text: str = "",
            icon: Optional[DialogIcon] = None,
            parent: Optional[QWidget] = None,
    ) -> None:
        """Initialize the message dialog.

        Args:
            title: Window title.
            text: Main dialog text.
            informative_text: Optional secondary explanatory text.
            icon: Optional standard dialog icon preset.
            parent: Optional parent widget.
        """
        super().__init__(
            title=title,
            text=text,
            informative_text=informative_text,
            icon=icon,
            parent=parent,
        )

        ok_btn = QPushButton("OK")
        ok_btn.setDefault(True)
        ok_btn.setAutoDefault(True)
        ok_btn.clicked.connect(self.accept)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(ok_btn)
        btn_layout.addStretch(1)

        self.add_layout(btn_layout)
        self.setFixedSize(self.sizeHint())


class InfoDialog(QDialog):
    """Rich-text dialog for longer informational content."""

    def __init__(
            self,
            title: str,
            html_text: str,
            icon: Optional[DialogIcon] = DialogIcon.INFORMATION,
            parent: Optional[QWidget] = None,
            copy_button: bool = True,
    ) -> None:
        """Initialize the rich informational dialog.

        Args:
            title: Window title.
            html_text: Rich HTML content shown in the text browser.
            icon: Optional standard dialog icon preset.
            parent: Optional parent widget.
            copy_button: Whether to include a button that copies the visible text.
        """
        super().__init__(parent)

        self.setWindowTitle(title)
        self.resize(560, 360)
        self.setMinimumSize(420, 260)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 16, 18, 16)
        main_layout.setSpacing(12)

        top_row = QHBoxLayout()
        top_row.setSpacing(12)
        if icon is not None:
            std_icon = self.style().standardIcon(icon.value)
            pixmap = std_icon.pixmap(32, 32)
            icon_label = QLabel()
            icon_label.setPixmap(pixmap)
            icon_label.setFixedSize(icon_label.sizeHint())
            top_row.addWidget(icon_label, alignment=Qt.AlignTop)

        title_label = _make_html_label(f"<b>{html.escape(title)}</b>")
        top_row.addWidget(title_label, 1, alignment=Qt.AlignVCenter)
        main_layout.addLayout(top_row)

        browser = QTextBrowser(self)
        browser.setOpenExternalLinks(True)
        browser.setReadOnly(True)
        browser.setTextInteractionFlags(Qt.TextBrowserInteraction)
        browser.setHtml(html_text)
        browser.moveCursor(QTextCursor.Start)
        self._browser = browser
        main_layout.addWidget(browser, 1)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)

        if copy_button:
            copy_btn = QPushButton("Copy")
            copy_btn.clicked.connect(self._copy_to_clipboard)
            btn_layout.addWidget(copy_btn)

        close_btn = QPushButton("Close")
        close_btn.setDefault(True)
        close_btn.setAutoDefault(True)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)

        main_layout.addLayout(btn_layout)

    def _copy_to_clipboard(self) -> None:
        """Copy the visible dialog text to the clipboard."""
        QGuiApplication.clipboard().setText(self._browser.toPlainText())


class AboutDialog(QDialog):
    """Qt-like dialog for application and author information."""

    def __init__(
            self,
            title: str,
            html_text: str,
            icon_path: Optional[str] = None,
            parent: Optional[QWidget] = None,
            heading: Optional[str] = None,
    ) -> None:
        """Initialize the about dialog layout and content.

        Args:
            title: Window title.
            html_text: Rich HTML body content.
            parent: Optional parent widget.
            heading: Optional plain-text heading shown above the body content.
        """
        super().__init__(parent)

        self.setWindowTitle(title)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(22, 18, 22, 18)
        main_layout.setSpacing(16)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(18)

        # Use standard information icon
        icon_label = QLabel()
        pixmap = _try_load_app_icon_pixmap(96, icon_path)
        if pixmap is None:
            std_icon = self.style().standardIcon(QStyle.SP_MessageBoxInformation)
            pixmap = std_icon.pixmap(64, 64)
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        icon_label.setFixedWidth(max(pixmap.width() + 8, 84))
        content_layout.addWidget(icon_label, 0, Qt.AlignTop)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)

        heading_label = QLabel(heading or title)
        heading_label.setTextFormat(Qt.PlainText)
        heading_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        heading_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        right_layout.addWidget(heading_label)

        body_label = _make_html_label(html_text)
        body_label.setWordWrap(True)
        right_layout.addWidget(body_label, 1)

        content_layout.addLayout(right_layout, 1)
        main_layout.addLayout(content_layout, 1)
        main_layout.addSpacing(10)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.setCenterButtons(True)
        button_box.accepted.connect(self.accept)
        main_layout.addWidget(button_box)

        self.setFixedSize(self.sizeHint())


class AskDialog(TitledDialogBase):
    """Confirmation dialog returning yes, no, or cancel."""

    def __init__(
            self,
            title: str,
            text: str,
            informative_text: str = "",
            yes_btn_label: str = "Yes",
            no_btn_label: Optional[str] = None,
            cancel_btn_label: str = "Cancel",
            parent: Optional[QWidget] = None,
    ) -> None:
        """Initialize the question dialog.

        Args:
            title: Window title.
            text: Main question text.
            informative_text: Optional secondary explanatory text.
            yes_btn_label: Label for the affirmative button.
            no_btn_label: Optional label for an explicit negative button.
            cancel_btn_label: Label for the cancel button.
            parent: Optional parent widget.
        """
        super().__init__(
            title=title,
            text=text,
            informative_text=informative_text,
            icon=DialogIcon.QUESTION,
            parent=parent,
        )

        self.result_value = AskResult.CANCEL

        yes_btn = QPushButton(yes_btn_label)
        cancel_btn = QPushButton(cancel_btn_label)

        yes_btn.setDefault(True)
        yes_btn.setAutoDefault(True)

        yes_btn.clicked.connect(self._yes)
        cancel_btn.clicked.connect(self.reject)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(yes_btn)
        if no_btn_label:
            no_btn = QPushButton(no_btn_label)
            no_btn.clicked.connect(self._no)
            btn_layout.addWidget(no_btn)
        btn_layout.addWidget(cancel_btn)

        self.add_layout(btn_layout)
        self.setFixedSize(self.sizeHint())

    def _yes(self) -> None:
        """Record an affirmative answer and close the dialog."""
        self.result_value = AskResult.YES
        self.accept()

    def _no(self) -> None:
        """Record a negative answer and close the dialog."""
        self.result_value = AskResult.NO
        self.accept()


# ---------------------------------------------------------------------------
# Convenience functions
# ---------------------------------------------------------------------------

def show_information(
        title: str,
        text: str,
        informative_text: str = "",
        parent: Optional[QWidget] = None,
) -> None:
    """Show an informational message dialog.

    Args:
        title: Window title.
        text: Main dialog text.
        informative_text: Optional secondary explanatory text.
        parent: Optional parent widget.
    """
    dlg = MessageDialog(title, text, informative_text, icon=DialogIcon.INFORMATION, parent=parent)
    dlg.exec()


def show_rich_information(
        title: str,
        html_text: str,
        parent: Optional[QWidget] = None,
        icon: Optional[DialogIcon] = DialogIcon.INFORMATION,
        copy_button: bool = True,
) -> None:
    """Show a rich-text informational dialog.

    Args:
        title: Window title.
        html_text: Rich HTML content.
        parent: Optional parent widget.
        icon: Optional standard dialog icon preset.
        copy_button: Whether to include a copy button.
    """
    dlg = InfoDialog(
        title=title,
        html_text=html_text,
        icon=icon,
        parent=parent,
        copy_button=copy_button,
    )
    dlg.exec()


def show_about_dialog(
        title: str,
        html_text: str,
        icon_path: Optional[str] = None,
        parent: Optional[QWidget] = None,
        heading: Optional[str] = None,
) -> None:
    """Show a Qt-like About dialog.

    Args:
        title: Window title.
        html_text: Rich HTML body content.
        parent: Optional parent widget.
        heading: Optional heading shown above the body content.
    """
    dlg = AboutDialog(title=title, html_text=html_text, icon_path=icon_path, parent=parent, heading=heading)
    dlg.exec()


def show_warning(
        title: str,
        text: str,
        informative_text: str = "",
        parent: Optional[QWidget] = None,
) -> None:
    """Show a warning message dialog.

    Args:
        title: Window title.
        text: Main warning text.
        informative_text: Optional secondary explanatory text.
        parent: Optional parent widget.
    """
    dlg = MessageDialog(title, text, informative_text, icon=DialogIcon.WARNING, parent=parent)
    dlg.exec()


def show_critical(
        title: str,
        text: str,
        informative_text: str = "",
        parent: Optional[QWidget] = None,
) -> None:
    """Show a critical-error message dialog.

    Args:
        title: Window title.
        text: Main error text.
        informative_text: Optional secondary explanatory text.
        parent: Optional parent widget.
    """
    dlg = MessageDialog(title, text, informative_text, icon=DialogIcon.CRITICAL, parent=parent)
    dlg.exec()


def ask_question(
        title: str,
        text: str,
        informative_text: str = "",
        yes_btn_label: str = "Yes",
        no_btn_label: Optional[str] = None,
        cancel_btn_label: str = "Cancel",
        parent: Optional[QWidget] = None,
) -> AskResult:
    """Show a confirmation dialog and return the selected answer.

    Args:
        title: Window title.
        text: Main question text.
        informative_text: Optional secondary explanatory text.
        yes_btn_label: Label for the affirmative button.
        no_btn_label: Optional label for an explicit negative button.
        cancel_btn_label: Label for the cancel button.
        parent: Optional parent widget.

    Returns:
        Selected dialog result.
    """
    dlg = AskDialog(
        title,
        text,
        informative_text,
        yes_btn_label=yes_btn_label,
        no_btn_label=no_btn_label,
        cancel_btn_label=cancel_btn_label,
        parent=parent,
    )
    dlg.exec()
    return dlg.result_value


def _demo_main() -> int:
    """Run the dialog module as a standalone demo.

    Returns:
        Qt application exit code.
    """
    import sys
    from PySide6.QtWidgets import QApplication, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

    class TestWindow(QWidget):
        """Test window for the dialog helpers."""

        def __init__(self) -> None:
            super().__init__()
            self.setWindowTitle("Dialog Demo")
            self.resize(500, 300)

            btn_info = QPushButton("show_information")
            btn_rich = QPushButton("show_rich_information")
            btn_about = QPushButton("show_about_dialog")
            btn_warning = QPushButton("show_warning")
            btn_critical = QPushButton("show_critical")
            btn_ask = QPushButton("ask_question")

            layout = QVBoxLayout(self)
            row = QHBoxLayout()
            for btn in (btn_info, btn_rich, btn_about, btn_warning, btn_critical, btn_ask):
                row.addWidget(btn)
            layout.addLayout(row)

            btn_info.clicked.connect(lambda: show_information("Info", "Everything looks good.", parent=self))
            btn_rich.clicked.connect(lambda: show_rich_information("Rich", "<b>Hello</b> world!", parent=self))
            btn_about.clicked.connect(lambda: show_about_dialog("About", "Version 1.0", heading="My App", parent=self))
            btn_warning.clicked.connect(lambda: show_warning("Warning", "This might be a problem.", parent=self))
            btn_critical.clicked.connect(lambda: show_critical("Error", "Something went wrong.", parent=self))
            btn_ask.clicked.connect(lambda: print(ask_question("Question", "Continue?", parent=self)))

    app = QApplication(sys.argv)
    w = TestWindow()
    w.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(_demo_main())
