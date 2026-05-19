"""Application entry point for the local translator."""

import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from translator.config import DEFAULT_FONT, DEFAULT_FONT_SIZE
from translator.themes import apply_light_theme
from translator.translator_app import TranslatorApp


def main():
    """Start the desktop application."""
    app = QApplication(sys.argv)

    font = QFont(DEFAULT_FONT, DEFAULT_FONT_SIZE)
    app.setFont(font)

    translator = TranslatorApp()
    apply_light_theme(app)
    translator.theme_button.setText("🌓")
    translator.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
