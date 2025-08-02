# utils/summarizer.py

from transformers import pipeline

# Load model once
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text, max_length=250, min_length=50):
    # Truncate if the text is too long
    if len(text.split()) > 1000:
        text = ' '.join(text.split()[:1000])
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']
