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
        self.delimiter = b'::KAVACH_ELITE_SIG::'

    def encrypt(self, text):
        cipher = AES.new(self.key, AES.MODE_CBC)
        return cipher.iv + cipher.encrypt(pad(zlib.compress(text.encode()), 16)) + self.delimiter

    def decrypt(self, blob):
        try:
            iv, data = blob[:16], blob[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return zlib.decompress(unpad(cipher.decrypt(data), 16)).decode()
        except: return None

# --- UI CONFIGURATION: HYPER-CYBER GLOW ---
st.set_page_config(page_title="Kavach Hyper-Cyber", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0a0e17 0%, #000000 100%);
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .hyper-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #39ff14, #bc13fe, #00f2ff, #39ff14);
        background-size: 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 8s linear infinite;
    }
    @keyframes glow { 0% { background-position: 0%; } 100% { background-position: 300%; } }

    .stTabs [data-baseweb="tab-list"] { gap: 30px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        font-family: 'Orbitron', sans-serif;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 5px;
        color: #888;
    }
    .stTabs [aria-selected="true"] {
        border: 1px solid #00f2ff !important;
        color: #00f2ff !important;
        box-shadow: 0px 0px 15px #00f2ff55;
    }

    .stButton>button {
        background: transparent;
        border: 2px solid #39ff14;
        color: #39ff14;
        font-family: 'Orbitron', sans-serif;
        border-radius: 0px;
        width: 100%;
        transition: 0.5s;
    }
    .stButton>button:hover {
        background: #39ff14;
        color: #000;
        box-shadow: 0 0 40px #39ff14;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="hyper-title">KAVACH ELITE</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #bc13fe; font-family: Orbitron;'><b>PROTOCOL: AES-256-CBC | ENGINE: HARDENED-LSB</b></p>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["[ SHIELD_ENCODE ]", "[ SENTRY_DECODE ]", "[ SYSTEM_AUDIT ]"])

# --- TAB 1: ENCODER (FIXED LINE 98 ERROR) ---
with t1:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.subheader("📡 PAYLOAD INJECTION")
        carrier = st.file_uploader("LOAD CARRIER (PNG)", type=["png"])
        secret = st.text_area("SECRET DATA", placeholder="Classified transmission...")
        key = st.text_input("ACCESS KEY", type="password")
        
    if st.button("EXECUTE ENCODING SEQUENCE") and carrier and secret and key:
        with st.status("Initiating Quantum Stealth...") as status:
            engine = KavachEngine(key)
            img = Image.open(carrier).convert('RGB')
            pixels = np.array(img)
            
            blob = engine.encrypt(secret)
            bits = np.unpackbits(np.frombuffer(blob, dtype=np.uint8))
            
            flat = pixels.flatten()
            if len(bits) > len(flat):
                st.error("⚠️ CAPACITY BREACH")
            else:
                # --- CORRECTED LOGIC FOR LINE 98 ---
                # We cast to int16 to prevent the OverflowError
                st.write("Applying 16-bit Hardened Mapping...")
                buffer_pixels = flat[:len(bits)].astype(np.int16) 
                # Injection happens in the larger 16-bit space
                buffer_pixels = (buffer_pixels & ~1) | bits 
                # Cast back to standard image format (uint8)
                flat[:len(bits)] = buffer_pixels.astype(np.uint8) 
                
                stego_img = Image.fromarray(flat.reshape(pixels.shape))
                
                # Metrics
                mse = np.mean((pixels.astype(np.float32) - flat.reshape(pixels.shape).astype(np.float32))**2)
                psnr = 100 if mse == 0 else 20 * math.log10(255.0 / math.sqrt(mse))
                
                with c2:
                    st.image(stego_img, use_container_width=True)
                    st.metric("FIDELITY (PSNR)", f"{psnr:.2f} dB")
                    buf = io.BytesIO()
                    stego_img.save(buf, format="PNG")
                    st.download_button("💾 DOWNLOAD SECURE_IMAGE.PNG", buf.getvalue(), "kavach_v6.png")
            status.update(label="Sequence Successful", state="complete")

# --- TAB 2: DECODER ---
with t2:
    st.subheader("🔍 DEEP SIGNAL SCAN")
    stego_in = st.file_uploader("UPLOAD STEGO-FRAME", type=["png"], key="dec")
    key_in = st.text_input("DECRYPT_KEY", type="password", key="key")
    
    if st.button("RUN EXTRACTION") and stego_in and key_in:
        engine = KavachEngine(key_in)
        img_d = Image.open(stego_in).convert('RGB')
        bits_d = np.array(img_d).flatten() & 1
        bytes_d = np.packbits(bits_d).tobytes()
        
        if engine.delimiter in bytes_d:
            raw = bytes_d.split(engine.delimiter)[0]
            result = engine.decrypt(raw)
            if result:
                st.success("✅ AUTHENTICATION VERIFIED")
                st.code(result)
            else: st.error("❌ KEY MISMATCH")
        else: st.error("⚠️ NO SIGNATURE DETECTED")

# --- TAB 3: AUDIT ---
with t3:
    st.subheader("⚙️ CORE ARCHITECTURE")
    st.markdown("""
    - **Stealth Engine:** Spatial Domain LSB mapping with 16-bit overflow protection.
    - **Encryption:** AES-256-CBC with randomized IV.
    - **Integrity:** PSNR-based visual audit layer.
    """)
    st.progress(1.0)
