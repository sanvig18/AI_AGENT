import streamlit as st
import numpy as np
from PIL import Image
import fitz  # PyMuPDF
import easyocr

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI OCR Companion",
    page_icon="📄",
    layout="wide"
)

# =========================
# LOAD OCR (CACHE FOR SPEED)
# =========================
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

# =========================
# SAFE VOICE FUNCTION (CLOUD FRIENDLY)
# =========================
def speak(text):
    st.info("🔊 Voice Output (Demo Mode):")
    st.markdown(f"### {text}")

# =========================
# UI HEADER
# =========================
st.markdown("## 📁 AI Accessibility OCR Companion")
st.write("Upload an image or PDF to extract and understand text.")

st.markdown("---")

uploaded_file = st.file_uploader(
    "Upload Image or PDF",
    type=["png", "jpg", "jpeg", "pdf"]
)

# =========================
# OCR FUNCTIONS
# =========================
def extract_text_from_image(img):
    result = reader.readtext(np.array(img))
    text = " ".join([r[1] for r in result])
    return text if text else "No text detected"

def extract_text_from_pdf(pdf_file):
    text = ""
    pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")

    for page in pdf:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        result = reader.readtext(np.array(img))
        text += " ".join([r[1] for r in result]) + "\n"

    return text if text.strip() else "No text detected in PDF"

# =========================
# MAIN LOGIC
# =========================
if uploaded_file is not None:

    file_type = uploaded_file.type

    # IMAGE OCR
    if "image" in file_type:
        image = Image.open(uploaded_file)

        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Uploaded Image", use_container_width=True)

        with col2:
            st.markdown("### 🧠 Extracted Text")

            extracted_text = extract_text_from_image(image)
            st.success(extracted_text)

            if st.button("🔊 Read Text"):
                speak(extracted_text)

    # PDF OCR
    elif "pdf" in file_type:

        st.info("Processing PDF...")

        extracted_text = extract_text_from_pdf(uploaded_file)

        st.markdown("### 🧠 Extracted Text from PDF")
        st.success(extracted_text)

        if st.button("🔊 Read Text"):
            speak(extracted_text)
