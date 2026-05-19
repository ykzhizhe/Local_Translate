"""Translation helpers shared by the GUI and CLI worker."""

import os
import re
import sys

import torch
import torch.nn as nn
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

from translator.config import MAX_INPUT_LENGTH, MODEL_NAME, MODEL_PATH

_MODEL = None
_TOKENIZER = None
_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_MODEL_LOAD_KWARGS = {
    "low_cpu_mem_usage": True,
}


def _load_model():
    """Load and cache the translation model and tokenizer."""
    global _MODEL, _TOKENIZER

    if _MODEL is not None and _TOKENIZER is not None:
        return _MODEL, _TOKENIZER

    has_local_model = os.path.exists(os.path.join(MODEL_PATH, "config.json"))
    model_source = MODEL_PATH if has_local_model else MODEL_NAME

    model = M2M100ForConditionalGeneration.from_pretrained(
        model_source,
        **_MODEL_LOAD_KWARGS,
    )
    tokenizer = M2M100Tokenizer.from_pretrained(model_source)
    model.to(_DEVICE)

    if _DEVICE.type == "cpu":
        try:
            model = torch.quantization.quantize_dynamic(
                model, {nn.Linear}, dtype=torch.qint8
            )
            print("已启用 CPU 动态量化以降低内存占用", file=sys.stderr)
        except Exception as exc:
            print(f"CPU 动态量化失败，继续使用原模型: {exc}", file=sys.stderr)

    model.eval()

    _MODEL = model
    _TOKENIZER = tokenizer
    return _MODEL, _TOKENIZER


def translate_text(text, source_lang, target_lang):
    """Translate a string between supported languages."""
    if source_lang == target_lang:
        return text

    model, tokenizer = _load_model()

    processed_text = text
    if len(processed_text) > MAX_INPUT_LENGTH:
        processed_text = processed_text[:MAX_INPUT_LENGTH] + "..."

    # Keep hyphenated words together when tokenizing dense technical text.
    processed_text = re.sub(r"(\w+)-(\w+)", r'"\1-\2"', processed_text)

    tokenizer.src_lang = source_lang
    inputs = tokenizer(
        processed_text,
        return_tensors="pt",
        max_length=512,
        truncation=True,
    )
    inputs = {key: value.to(_DEVICE) for key, value in inputs.items()}

    with torch.inference_mode():
        generated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.get_lang_id(target_lang),
            max_new_tokens=128,
        )

    result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return result[0] if result else "翻译失败"
