from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load model
tokenizer = AutoTokenizer.from_pretrained("t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

def rewrite_text(text, tone="easy"):
    """
    Rewrite the input text based on the tone: 'easy', 'formal', or 'casual'.
    """
    prompt_map = {
        "easy": "Simplify this: ",
        "formal": "Make this formal: ",
        "casual": "Make this casual: "
    }

    prompt = prompt_map.get(tone.lower(), "Simplify this: ") + text

    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs, max_length=512, do_sample=True, top_k=50)
    rewritten = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return rewritten

