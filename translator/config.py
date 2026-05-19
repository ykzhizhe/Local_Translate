"""Translator configuration constants."""

import os

# Application configuration
APP_TITLE = "本地翻译器"
APP_WIDTH = 900
APP_HEIGHT = 500
APP_MIN_WIDTH = 800
APP_MIN_HEIGHT = 450

# Translation model configuration
MODEL_NAME = "facebook/m2m100_418M"
MODEL_PATH = os.path.abspath("./models")
USE_LOCAL_MODEL = os.path.exists(os.path.join(MODEL_PATH, "config.json"))
MAX_INPUT_LENGTH = 500

# Supported languages for the selected model and UI
LANGUAGES = {
    "中文": "zh",
    "英文": "en",
    "日文": "ja",
}

DEFAULT_SOURCE_LANGUAGE = "英文"
DEFAULT_TARGET_LANGUAGE = "中文"

# Default font
DEFAULT_FONT = "Microsoft YaHei UI"
DEFAULT_FONT_SIZE = 10

# UI text
TEXT_READY = "就绪"
TEXT_TRANSLATING = "正在翻译..."
TEXT_TRANSLATION_COMPLETE = "翻译完成"
TEXT_TRANSLATION_FAILED = "翻译失败"
TEXT_PREPARING = "准备翻译..."
TEXT_INPUT_PLACEHOLDER = "请在此输入要翻译的文本..."
TEXT_OUTPUT_PLACEHOLDER = "翻译结果将显示在这里..."
TEXT_WARNING = "警告"
TEXT_EMPTY_INPUT = "请输入要翻译的文本"
TEXT_PROGRESS = "翻译进度:"
TEXT_TRANSLATE = "翻译"
TEXT_CLEAR = "清除"
TEXT_INPUT = "输入"
TEXT_OUTPUT = "翻译结果"
TEXT_SOURCE_LANG = "源语言:"
TEXT_TARGET_LANG = "目标语言:"
TEXT_THEME_TOOLTIP = "切换主题"
TEXT_COPY = "复制"
TEXT_COPY_TOOLTIP = "复制到剪贴板"
TEXT_COPIED = "已复制到剪贴板"
TEXT_INPUT_TOO_LONG = "输入文本过长"
TEXT_INPUT_LENGTH_WARNING = (
    f"输入文本超过{MAX_INPUT_LENGTH}字符限制，将自动截断。\n\n是否继续翻译？"
)
TEXT_INPUT_LENGTH_INFO = f"当前字符数: {{}} / {MAX_INPUT_LENGTH}"
TEXT_SAME_LANGUAGE = "源语言和目标语言相同，已直接返回原文"
