import os

import torch
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

MODEL_NAME = "facebook/m2m100_418M"
MODEL_PATH = os.path.abspath("./models")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_source = MODEL_PATH if os.path.exists(os.path.join(MODEL_PATH, "config.json")) else MODEL_NAME

model = M2M100ForConditionalGeneration.from_pretrained(model_source)
model.to(DEVICE)
model.eval()

tokenizer = M2M100Tokenizer.from_pretrained(model_source)

source_lang = "en"
target_lang = "zh"
text = "This application now supports translation between Chinese, English, and Japanese."

tokenizer.src_lang = source_lang
inputs = tokenizer(text, return_tensors="pt")
inputs = {key: value.to(DEVICE) for key, value in inputs.items()}

generated_tokens = model.generate(
    **inputs,
    forced_bos_token_id=tokenizer.get_lang_id(target_lang),
)

result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
print(result[0] if result else "")
