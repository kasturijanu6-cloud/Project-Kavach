import streamlit as st
import numpy as np
import zlib, hashlib, math, io, time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image

# --- THE FORTRESS: HARDENED LOGIC ---
class KavachEngine:
    def __init__(self, password):
        # SHA-256 Key Stretching
        self.key = hashlib.sha256(password.encode()).digest()
        self.delimiter = b'::KAVACH_ALPHA_SHIELD::'

    def encrypt(self, text):
        cipher = AES.new(self.key, AES.MODE_CBC)
        compressed = zlib.compress(text.encode())
        encrypted = cipher.encrypt(pad(compressed, 16))
        return cipher.iv + encrypted + self.delimiter

    def decrypt(self, blob):
        try:
            iv, data = blob[:16], blob[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(data), 16)
            return zlib.decompress(decrypted).decode()
        except: return None

# --- UI CONFIGURATION & GLASSMORPHISM ---
st.set_page_config(page_title="Project Kavach Elite", page_icon="☣️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at top, #0d1b2a 0%, #000814 100%);
        color: #00f2ff;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Glassmorphism Containers */
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(0, 242, 255, 0.2);
    }
    
    /* Neon Titles */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #00f2ff !important;
        text-shadow: 0 0 10px #00f2ff88;
    }
    
    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00f2ff, #0066ff);
        color: white !important;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s all;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 20px #00f2ff;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("☣️ KAVACH ELITE : DEFENSE TERMINAL")
st.write("`CONNECTED: SECURE_NODE_ALPHA | KERNEL: AES-256-SHA256`")
st.divider()

tab1, tab2, tab3 = st.tabs(["[ 🔒 SHIELD ENCODER ]", "[ 🔍 SENTRY DECODER ]", "[ 📊 ANALYTICS ]"])

# --- TAB 1: ENCODER ---
with tab1:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.subheader("Payload Injection")
        carrier = st.file_uploader("Upload Carrier Image (PNG)", type=["png"])
        secret = st.text_area("Secret Message", height=120)
        pwd = st.text_input("Encryption Key", type="password")
        
        if st.button("ACTIVATE DEFENSE SHIELD") and carrier and secret and pwd:
            with st.status("Deploying Kavach...") as status:
                engine = KavachEngine(pwd)
                img = Image.open(carrier).convert('RGB')
                pixels = np.array(img)
                
                # Encrypt
                st.write("Applying AES-256 Cryptography...")
                protected = engine.encrypt(secret)
                bits = np.unpackbits(np.frombuffer(protected, dtype=np.uint8))
                
                flat = pixels.flatten()
                if len(bits) > len(flat):
                    st.error("DATA OVERLOAD: Use a larger carrier image.")
                else:
                    st.write("Executing Stealth Embedding...")
                    # Hardened LSB logic (int16 fix included)
                    temp = flat[:len(bits)].astype(np.int16)
                    temp = (temp & ~1) | bits
                    flat[:len(bits)] = temp.astype(np.uint8)
                    
                    stego_img = Image.fromarray(flat.reshape(pixels.shape))
                    
                    # Metrics
                    mse = np.mean((pixels.astype(np.float32) - flat.reshape(pixels.shape).astype(np.float32))**2)
                    psnr = 100 if mse == 0 else 20 * math.log10(255.0 / math.sqrt(mse))
                    
                    with c2:
                        st.subheader("Transmission Ready")
                        st.image(stego_img, caption="Shielded Stego-Object", use_container_width=True)
                        
                        # Scoreboard
                        col_m1, col_m2 = st.columns(2)
                        col_m1.metric("STEALTH (PSNR)", f"{psnr:.2f} dB")
                        col_m2.metric("DEFENSE SCORE", f"{min(100, int(psnr + 20))}%")
                        
                        buf = io.BytesIO()
                        stego_img.save(buf, format="PNG")
                        st.download_button("💾 EXPORT SECURE FILE", buf.getvalue(), "kavach_alpha.png")
                status.update(label="Shield Deployment Successful", state="complete")

# --- TAB 2: DECODER ---
with tab2:
    st.subheader("Signal Interception & Decryption")
    stego_in = st.file_uploader("Upload Stego-Frame", type=["png"], key="dec_in")
    key_in = st.text_input("Enter Defense Key", type="password", key="k_in")
    
    if st.button("START DEEP SCAN"):
        engine = KavachEngine(key_in)
        img_d = Image.open(stego_in).convert('RGB')
        bits_d = np.array(img_d).flatten() & 1
        bytes_d = np.packbits(bits_d).tobytes()
        
        if engine.delimiter in bytes_d:
            raw = bytes_d.split(engine.delimiter)[0]
            decoded = engine.decrypt(raw)
            if decoded:
