import streamlit as st
import numpy as np
import zlib
import hashlib
import math
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import io

# --- UI CONFIGURATION & STYLING ---
st.set_page_config(page_title="Project Kavach", page_icon="🛡️", layout="wide")

# This CSS adds the "Dark Mode / Cyberpunk" aesthetic
st.markdown("""
    <style>
    /* Main background and font */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #e0e0e0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00ffcc !important;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 2px 2px 4px #000000;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: rgba(0, 0, 0, 0.3);
        padding: 10px;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px;
        color: #ffffff;
        font-weight: bold;
    }

    .stTabs [aria-selected="true"] {
        background-color: #00ffcc22 !important;
        border-bottom: 2px solid #00ffcc !important;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        background-color: #00ffcc;
        color: #000;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #00ccaa;
        box-shadow: 0 0 15px #00ffcc;
        color: white;
    }

    /* Input boxes */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #161b22 !important;
        color: #00ffcc !important;
        border: 1px solid #30363d !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col_h1, col_h2 = st.columns([1, 4])
with col_h1:
    st.title("🛡️")
with col_h2:
    st.title("PROJECT KAVACH")
    st.markdown("#### **Status:** SYSTEM READY | **Encryption:** AES-256")

st.divider()
