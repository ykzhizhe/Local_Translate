"""Main PyQt application window."""

import json
import os
import subprocess
import sys

from PyQt6.QtCore import QPoint, Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from translator.config import (
    APP_HEIGHT,
    APP_MIN_HEIGHT,
    APP_MIN_WIDTH,
    APP_TITLE,
    APP_WIDTH,
    DEFAULT_SOURCE_LANGUAGE,
    DEFAULT_TARGET_LANGUAGE,
    LANGUAGES,
    MAX_INPUT_LENGTH,
    TEXT_CLEAR,
    TEXT_COPIED,
    TEXT_COPY_TOOLTIP,
    TEXT_EMPTY_INPUT,
    TEXT_INPUT,
    TEXT_INPUT_LENGTH_INFO,
    TEXT_INPUT_LENGTH_WARNING,
    TEXT_INPUT_PLACEHOLDER,
    TEXT_INPUT_TOO_LONG,
    TEXT_OUTPUT,
    TEXT_OUTPUT_PLACEHOLDER,
    TEXT_PREPARING,
    TEXT_PROGRESS,
    TEXT_READY,
    TEXT_SOURCE_LANG,
    TEXT_TARGET_LANG,
    TEXT_THEME_TOOLTIP,
    TEXT_TRANSLATE,
    TEXT_TRANSLATING,
    TEXT_TRANSLATION_COMPLETE,
    TEXT_TRANSLATION_FAILED,
    TEXT_WARNING,
)
from translator.themes import apply_dark_theme, apply_light_theme


class DownComboBox(QComboBox):
    """Force the dropdown menu to open below the combo box."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaxVisibleItems(5)
        self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

    def showPopup(self):
        super().showPopup()
        QTimer.singleShot(0, self._adjust_popup_position)

    def _adjust_popup_position(self):
        popup = self.view()
        if not popup:
            return

        popup_window = popup.window()
        if not popup_window:
            return

        global_pos = self.mapToGlobal(QPoint(0, 0))
        popup_window.move(global_pos.x(), global_pos.y() + self.height())
        popup_window.resize(max(popup_window.width(), self.width()), popup_window.height())


class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_dark_theme = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, APP_WIDTH, APP_HEIGHT)
        self.setMinimumSize(APP_MIN_WIDTH, APP_MIN_HEIGHT)

        try:
            logo_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "ui", "logo.png"
            )
            if os.path.exists(logo_path):
                self.setWindowIcon(QIcon(logo_path))
        except Exception as exc:
            print(f"无法加载 logo: {exc}")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(5)

        left_group = QGroupBox(TEXT_INPUT)
        left_layout = QVBoxLayout(left_group)

        source_lang_layout = QHBoxLayout()
        self.source_lang_label = QLabel(TEXT_SOURCE_LANG)
        self.source_lang_combo = DownComboBox()
        for lang, code in LANGUAGES.items():
            self.source_lang_combo.addItem(f"{lang} ({code})")
        self.source_lang_combo.setCurrentText(
            f"{DEFAULT_SOURCE_LANGUAGE} ({LANGUAGES[DEFAULT_SOURCE_LANGUAGE]})"
        )
        source_lang_layout.addWidget(self.source_lang_label)
        source_lang_layout.addWidget(self.source_lang_combo)
        source_lang_layout.addStretch(1)
        left_layout.addLayout(source_lang_layout)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText(TEXT_INPUT_PLACEHOLDER)
        self.input_text.textChanged.connect(self.update_character_count)
        left_layout.addWidget(self.input_text)

        self.char_count_label = QLabel(TEXT_INPUT_LENGTH_INFO.format(0))
        self.char_count_label.setStyleSheet("color: gray; font-size: 10px;")
        left_layout.addWidget(self.char_count_label)

        content_layout.addWidget(left_group)

        middle_layout = QVBoxLayout()
        middle_layout.setSpacing(5)
        middle_layout.setContentsMargins(2, 2, 2, 2)
        middle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.theme_button = QPushButton()
        self.theme_button.setFixedSize(28, 28)
        self.theme_button.setToolTip(TEXT_THEME_TOOLTIP)
        self.theme_button.setObjectName("themeButton")
        self.theme_button.setText("🌓")
        self.theme_button.clicked.connect(self.toggle_theme)

        theme_button_layout = QHBoxLayout()
        theme_button_layout.addWidget(
            self.theme_button, 0, Qt.AlignmentFlag.AlignCenter
        )
        middle_layout.addLayout(theme_button_layout)
        middle_layout.addStretch(1)

        self.translate_button = QPushButton(TEXT_TRANSLATE)
        self.translate_button.setFixedWidth(80)
        self.translate_button.setFixedHeight(32)
        self.translate_button.clicked.connect(self.start_translation)
        middle_layout.addWidget(self.translate_button, 0, Qt.AlignmentFlag.AlignCenter)

        self.clear_button = QPushButton(TEXT_CLEAR)
        self.clear_button.setFixedWidth(80)
        self.clear_button.setFixedHeight(32)
        self.clear_button.clicked.connect(self.clear_text)
        middle_layout.addWidget(self.clear_button, 0, Qt.AlignmentFlag.AlignCenter)

        middle_layout.addStretch(1)
        content_layout.addLayout(middle_layout)

        right_group = QGroupBox(TEXT_OUTPUT)
        right_layout = QVBoxLayout(right_group)

        target_lang_layout = QHBoxLayout()
        self.target_lang_label = QLabel(TEXT_TARGET_LANG)
        self.target_lang_combo = DownComboBox()
        for lang, code in LANGUAGES.items():
            self.target_lang_combo.addItem(f"{lang} ({code})")
        self.target_lang_combo.setCurrentText(
            f"{DEFAULT_TARGET_LANGUAGE} ({LANGUAGES[DEFAULT_TARGET_LANGUAGE]})"
        )
        target_lang_layout.addWidget(self.target_lang_label)
        target_lang_layout.addWidget(self.target_lang_combo)
        target_lang_layout.addStretch(1)
        right_layout.addLayout(target_lang_layout)

        output_container = QWidget()
        output_container_layout = QVBoxLayout(output_container)
        output_container_layout.setContentsMargins(0, 0, 0, 0)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText(TEXT_OUTPUT_PLACEHOLDER)
        output_container_layout.addWidget(self.output_text)

        copy_button_layout = QHBoxLayout()
        copy_button_layout.addStretch(1)

        self.copy_button = QToolButton()
        self.copy_button.setToolTip(TEXT_COPY_TOOLTIP)
        self.copy_button.setText("📋")
        self.copy_button.setFixedSize(28, 28)
        self.copy_button.setObjectName("copyButton")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setCursor(Qt.CursorShape.PointingHandCursor)
        copy_button_layout.addWidget(self.copy_button)

        output_container_layout.addLayout(copy_button_layout)
        right_layout.addWidget(output_container)

        content_layout.addWidget(right_group)
        main_layout.addLayout(content_layout)

        status_layout = QHBoxLayout()
        self.status_label = QLabel(TEXT_READY)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch(1)

        progress_layout = QHBoxLayout()
        progress_layout.addWidget(QLabel(TEXT_PROGRESS))

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(200)
        progress_layout.addWidget(self.progress_bar)

        status_layout.addLayout(progress_layout)
        main_layout.addLayout(status_layout)

    def update_character_count(self):
        """Update the visible character counter."""
        text = self.input_text.toPlainText()
        char_count = len(text)
        self.char_count_label.setText(TEXT_INPUT_LENGTH_INFO.format(char_count))

        if char_count > MAX_INPUT_LENGTH:
            self.char_count_label.setStyleSheet(
                "color: red; font-size: 10px; font-weight: bold;"
            )
        elif char_count > MAX_INPUT_LENGTH * 0.8:
            self.char_count_label.setStyleSheet("color: orange; font-size: 10px;")
        else:
            self.char_count_label.setStyleSheet("color: gray; font-size: 10px;")

    def start_translation(self):
        text = self.input_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, TEXT_WARNING, TEXT_EMPTY_INPUT)
            return

        if len(text) > MAX_INPUT_LENGTH:
            reply = QMessageBox.question(
                self,
                TEXT_INPUT_TOO_LONG,
                TEXT_INPUT_LENGTH_WARNING,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
            if reply == QMessageBox.StandardButton.No:
                return

        source_lang = self.source_lang_combo.currentText().split("(")[1].strip(")")
        target_lang = self.target_lang_combo.currentText().split("(")[1].strip(")")

        self.status_label.setText(TEXT_PREPARING)
        self.translate_button.setEnabled(False)
        self.status_label.setText(TEXT_TRANSLATING)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(10)
        QApplication.processEvents()

        try:
            child_env = os.environ.copy()
            child_env["PYTHONIOENCODING"] = "utf-8"
            child_env["PYTHONUTF8"] = "1"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "translator.translate_cli",
                ],
                input=json.dumps(
                    {
                        "text": text,
                        "source_lang": source_lang,
                        "target_lang": target_lang,
                    },
                    ensure_ascii=False,
                ),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=child_env,
            )
            payload = json.loads((result.stdout or "").strip() or "{}")
            if payload.get("ok"):
                translated_text = payload.get("result", "")
            else:
                error = payload.get("error") or (result.stderr or "").strip() or "未知错误"
                raise RuntimeError(error)

            self.progress_bar.setValue(100)
            self.update_translation(translated_text)
        except Exception as exc:
            self.progress_bar.setValue(0)
            self.update_translation(f"翻译出错: {exc}")
        finally:
            self.translate_button.setEnabled(True)

    def update_translation(self, text):
        self.output_text.setText(text)
        if text.startswith("翻译出错"):
            self.status_label.setText(TEXT_TRANSLATION_FAILED)
            self.progress_bar.setValue(0)
        else:
            self.status_label.setText(TEXT_TRANSLATION_COMPLETE)
            self.progress_bar.setValue(100)

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        if value == 0:
            self.status_label.setText(TEXT_TRANSLATION_FAILED)
        elif value < 100:
            self.status_label.setText(TEXT_TRANSLATING)
        else:
            self.status_label.setText(TEXT_TRANSLATION_COMPLETE)

    def clear_text(self):
        self.input_text.clear()
        self.output_text.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText(TEXT_READY)

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.is_dark_theme = not self.is_dark_theme

        if self.is_dark_theme:
            apply_dark_theme(QApplication.instance())
            self.theme_button.setText("☀")
        else:
            apply_light_theme(QApplication.instance())
            self.theme_button.setText("🌓")

    def copy_to_clipboard(self):
        """Copy translated text to the clipboard."""
        text = self.output_text.toPlainText()
        if not text:
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(text)

        original_status = self.status_label.text()
        self.status_label.setText(TEXT_COPIED)
        QTimer.singleShot(1500, lambda: self.status_label.setText(original_status))
