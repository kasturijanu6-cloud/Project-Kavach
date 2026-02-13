import streamlit as st
import numpy as np
import zlib, hashlib, math, io, time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image

# --- THE FORTRESS: CRYPTO LOGIC ---
class KavachEngine:
    def __init__(self, password):
        self.key = hashlib.sha256(password.encode()).digest()
        self.delimiter = b'::KAVACH_EOS::'

    def encrypt(self, text):
        cipher = AES.new(self.key, AES.MODE_CBC)
        blob = cipher.iv + cipher.encrypt(pad(zlib.compress(text.encode()), 16)) + self.delimiter
        return blob

    def decrypt(self, blob):
        try:
            iv, data = blob[:16], blob[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return zlib.decompress(unpad(cipher.decrypt(data), 16)).decode()
        except: return None

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Project Kavach", page_icon="☣️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    * { font-family: 'JetBrains Mono', monospace; }
    .stApp { background-color: #050505; color: #00FF41; }
    .css-1offfwp { background-color: #111 !important; border: 1px solid #00FF41; }
    .terminal-text { color: #00FF41; font-size: 14px; line-height: 1.2; }
    </style>
""", unsafe_allow_html=True)

# --- APP LAYOUT ---
st.title("☣️ KAVACH-OS v2.0")
st.caption("SECURE QUANTUM-READY STEGANOGRAPHY TERMINAL")

tab_enc, tab_dec, tab_sys = st.tabs(["[ SHIELD_ENCODE ]", "[ SENTRY_DECODE ]", "[ SYSTEM_LOGS ]"])

with tab_enc:
    col_in, col_out = st.columns([1, 1])
    with col_in:
        st.subheader("📡 Input Stream")
        carrier = st.file_uploader("Upload Carrier Frame (PNG)", type=["png"])
        msg = st.text_area("Secure Payload", height=100)
        key = st.text_input("Access Key", type="password")
        
    if st.button("EXECUTE ENCODING SEQUENCE") and carrier and msg and key:
        with st.status("Initializing Phantom-Shield...") as status:
            engine = KavachEngine(key)
            img = Image.open(carrier).convert('RGB')
            pixels = np.array(img, dtype=np.uint16) # Use 16-bit to prevent overflow
            
            status.update(label="Encrypting Payload...", state="running")
            blob = engine.encrypt(msg)
            bits = np.unpackbits(np.frombuffer(blob, dtype=np.uint8))
            
            if len(bits) > pixels.size:
                st.error("SYSTEM ERROR: Payload exceeds carrier capacity.")
            else:
                status.update(label="Injecting Bits into LSB Space...", state="running")
                flat = pixels.flatten()
                flat[:len(bits)] = (flat[:len(bits)] & 254) | bits
                stego = flat.reshape(pixels.shape).astype(np.uint8)
                
                # Analysis
                mse = np.mean((pixels.astype(np.float32) - stego.astype(np.float32))**2)
                psnr = 20 * math.log10(255.0 / math.sqrt(mse)) if mse > 0 else 100
                
                with col_out:
                    st.subheader("🛰️ Stego-Object Ready")
                    st.image(stego, use_container_width=True)
                    st.metric("Visual Integrity (PSNR)", f"{psnr:.2f} dB")
                    
                    buf = io.BytesIO()
                    Image.fromarray(stego).save(buf, format="PNG")
                    st.download_button("💾 EXPORT SECURE_IMAGE.PNG", buf.getvalue(), "kavach_v2.png")
            status.update(label="Sequence Complete", state="complete")

with tab_dec:
    st.subheader("🔍 Signal Analysis")
    stego_in = st.file_uploader("Upload Stego-Frame", type=["png"], key="dec")
    key_in = st.text_input("Defense Key", type="password", key="k2")
    
    if st.button("RUN DEEP-SCAN"):
        engine = KavachEngine(key_in)
        img_dec = Image.open(stego_in).convert('RGB')
        bits_dec = np.array(img_dec).flatten() & 1
        bytes_dec = np.packbits(bits_dec).tobytes()
        
        if engine.delimiter in bytes_dec:
            clean_blob = bytes_dec.split(engine.delimiter)[0]
            result = engine.decrypt(clean_blob)
            if result:
                st.success("✅ DECRYPTION SUCCESSFUL")
                st.code(result, language="text")
            else: st.error("❌ KEY MISMATCH: Access Denied.")
        else: st.error("⚠️ NO KAVACH SIGNATURE DETECTED.")

with tab_sys:
    st.subheader("⚙️ Hardware Specs & Architecture")
    st.markdown("""
    - **Kernel:** AES-256-CBC with SHA-256 Key Stretching.
    - **Capacity:** Calculated based on bit-depth per color channel.
    - **Method:** Spatial Domain LSB Substitution (Visual Track).
    - **Integrity:** 16-byte IV randomized per session.
    """)
    st.write("System Uptime: Running in Hackathon Battle Mode.")
