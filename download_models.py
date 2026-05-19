import os

from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

MODEL_NAME = "facebook/m2m100_418M"
MODEL_PATH = os.path.abspath("./models")

os.makedirs(MODEL_PATH, exist_ok=True)

model = M2M100ForConditionalGeneration.from_pretrained(MODEL_NAME)
tokenizer = M2M100Tokenizer.from_pretrained(MODEL_NAME)

model.save_pretrained(MODEL_PATH)
tokenizer.save_pretrained(MODEL_PATH)

print(f"Model saved to {MODEL_PATH}")
