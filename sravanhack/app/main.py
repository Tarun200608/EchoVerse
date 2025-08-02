import os
import streamlit as st
from PyPDF2 import PdfReader
from streamlit_lottie import st_lottie
from utils.text_loader import load_text
from utils.rewriter import rewrite_text
from utils.summarizer import summarize_text
from utils.tts import text_to_speech
import base64
import json


# Set page config
st.set_page_config(page_title="EchoVerse", layout="centered")
st.markdown("<h1 style='text-align: center;'>📚 EchoVerse – AI Audiobook Generator</h1>", unsafe_allow_html=True)

# Load Lottie animation
def load_lottie_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

lottie_animation = load_lottie_file("assets/book.json")
st_lottie(lottie_animation, speed=1, height=250, key="intro")

# Upload PDF or type text
st.sidebar.header("📤 Upload or Paste Text")
pdf_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])
manual_text = st.sidebar.text_area("Or paste your own text")

if pdf_file is not None:
    extracted_text = load_text(pdf_file)
elif manual_text:
    extracted_text = manual_text
else:
    extracted_text = ""

# Mode selection
mode = st.sidebar.radio("Choose Mode", ("Rewrite", "Summarize", "Rewrite + Audio"))

# Tone options for rewriting
tone = st.sidebar.selectbox("Rewrite Tone", ("Casual", "Formal", "Easy"))

# Process Button
if st.sidebar.button("✨ Process Text"):
    if not extracted_text.strip():
        st.warning("Please upload a PDF or enter some text.")
    else:
        st.markdown("### ✍️ Original Text")
        st.text_area("Original", extracted_text, height=200)

        if mode == "Summarize":
            result = summarize_text(extracted_text)
            st.markdown("### 📌 Summarized Text")
            st.text_area("Summary", result, height=200)

        elif mode == "Rewrite":
            result = rewrite_text(extracted_text, tone)
            st.markdown("### ✨ Rewritten Text")
            st.text_area("Rewritten", result, height=200)

        elif mode == "Rewrite + Audio":
            rewritten = rewrite_text(extracted_text, tone)
            st.markdown("### ✨ Rewritten Text")
            st.text_area("Rewritten", rewritten, height=200)

            st.markdown("### 🔊 Audio Narration")
            audio_file_path = text_to_speech(rewritten)
            with open(audio_file_path, "rb") as f:
                audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mp3")

                # Download button
                b64 = base64.b64encode(audio_bytes).decode()
                href = f'<a href="data:audio/mp3;base64,{b64}" download="output.mp3">📥 Download Audio</a>'
                st.markdown(href, unsafe_allow_html=True)
