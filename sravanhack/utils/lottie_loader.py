import requests
import streamlit as st

@st.cache_data(show_spinner=False)
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
