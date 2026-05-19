# LocalTranslator

基于 PyQt6 和 Hugging Face Transformers 的本地桌面翻译器。

## 功能

- 本地离线翻译
- 支持中文、英文、日文互译
- 源语言和目标语言都会真正参与翻译
- 亮色与暗色主题
- 字符计数和长度提醒

## 模型

- 模型：`facebook/m2m100_418M`
- 后端：`transformers`
- 支持方向：中文 ↔ 英文、中文 ↔ 日文、英文 ↔ 日文

## 运行

```bash
uv sync
python download_models.py
python main.py
```

## 说明

- 新模型会比旧的 T5 方案更大。
- 应用现在会在首次加载后缓存模型，连续翻译时速度会更稳定。
