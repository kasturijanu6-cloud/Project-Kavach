import streamlit as st
import numpy as np
import zlib, hashlib, math, io, time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image

# --- THE CORE ENGINE ---
class KavachEngine:
    def __init__(self, password):
        self.key = hashlib.sha256(password.encode()).digest()
        self.delimiter = b'::PRISM_GUARD_SECURE::'

    def encrypt(self, text):
        cipher = AES.new(self.key, AES.MODE_CBC)
        return cipher.iv + cipher.encrypt(pad(zlib.compress(text.encode()), 16)) + self.delimiter

    def decrypt(self, blob):
        try:
            iv, data = blob[:16], blob[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return zlib.decompress(unpad(cipher.decrypt(data), 16)).decode()
        except: return None

# --- UI CONFIGURATION & CSS (FIXED SYNTAX) ---
st.set_page_config(page_title="Kavach Prism Defense", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Space+Grotesk:wght@300;500&display=swap');
    
    .stApp {
        background: linear-gradient(125deg, #050505 0%, #0a0a12 50%, #050505 100%);
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .prism-title {
        font-family: 'Syncopate', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        background: linear-gradient(90deg, #00f2ff, #7000ff, #ff0055);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }

    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px;
        margin-top: 20px;
    }

    .stButton>button {
        background: transparent;
        border: 2px solid #00f2ff;
        color: #00f2ff;
        border-radius: 50px;
        padding: 10px 40px;
        font-weight: bold;
        transition: 0.4s;
        width: 100%;
    }
    .stButton>button:hover {
        background: #00f2ff;
        color: #000;
        box-
