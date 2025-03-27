import torch
from transformers import pipeline
import textwrap

# Check if GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load AI summarization model (forcing GPU usage)
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=0 if device == "cuda" else -1
)

def ai_summarize(text):
    max_input_chars = 3000
    if len(text) > max_input_chars:
        text = text[:max_input_chars]
    if len(text) < 300:
        return text
    # Dynamically adjust max_length based on input length.
    if len(text) < 500:
        dynamic_max_length = 217
    else:
        dynamic_max_length = min(len(text) // 4, 512)
    min_length = max(100, dynamic_max_length // 2)
    try:
        summary = summarizer(
            text,
            max_length=dynamic_max_length,
            min_length=min_length,
            do_sample=False
        )[0]['summary_text']
        return textwrap.fill(summary, width=80)
    except Exception as e:
        print(f"Summarization failed: {e}")
        fallback = text[:1000] + "..."
        return textwrap.fill(fallback, width=80)
