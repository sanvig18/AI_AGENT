import streamlit as st
import speech_recognition as sr
import pyttsx3
import requests
import wikipedia
import cv2
import easyocr
import json
import os
import threading

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Accessibility Assistant", layout="wide")

st.title("♿ AI Accessibility Assistant (Voice + Vision + Memory)")

# =========================
# MEMORY SYSTEM
# =========================
MEM_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEM_FILE):
        return json.load(open(MEM_FILE))
    return {"history": []}

def save_memory(mem):
    json.dump(mem, open(MEM_FILE, "w"), indent=2)

memory = load_memory()

# =========================
# 🔊 TEXT TO SPEECH (TTS)
# =========================
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run).start()

# =========================
# 🎤 SPEECH TO TEXT (STT)
# =========================
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now")
        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=6, phrase_time_limit=6)
            text = r.recognize_google(audio)
            return text.lower()

        except:
            return ""

# =========================
# TOOLS
# =========================
def get_weather(city):
    try:
        return requests.get(f"https://wttr.in/{city}?format=3").text
    except:
        return "Weather unavailable"

def get_info(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except:
        return "No information found"

# =========================
# AI BRAIN
# =========================
def ai_brain(text):

    text = text.lower().strip()

    if text == "":
        return "I didn't hear you properly. Please try again."

    if "weather" in text:
        city = text.split("in")[-1].strip() if "in" in text else "delhi"
        return get_weather(city)

    if "who is" in text or "what is" in text:
        return get_info(text)

    if "help" in text:
        return "Say weather in Delhi, who is AI, or just speak naturally"

    if "route" in text:
        return "Navigation feature coming next upgrade with OSRM"

    return f"I understood: {text}"

# =========================
# VISION SYSTEM
# =========================
reader = easyocr.Reader(['en'])

def vision(frame):
    result = reader.readtext(frame)
    text = " ".join([r[1] for r in result])
    return text if text else "No text detected"

# =========================
# UI
# =========================
col1, col2 = st.columns(2)

# =========================
# 🎤 VOICE MODE (FULL FIXED)
# =========================
with col1:
    st.subheader("🎤 Voice Assistant")

    if st.button("Start Voice Input"):
        user_text = listen()

        st.write("🗣️ You said:", user_text)

        response = ai_brain(user_text)

        st.write("🤖 AI:", response)

        memory["history"].append({"user": user_text, "ai": response})
        save_memory(memory)

        # 🔊 Speak response
        speak(response)

# =========================
# ⌨️ TEXT MODE
# =========================
with col2:
    st.subheader("⌨️ Text Assistant")

    text = st.text_input("Type here")

    if st.button("Send"):
        response = ai_brain(text)

        st.write("🤖 AI:", response)

        memory["history"].append({"user": text, "ai": response})
        save_memory(memory)

        speak(response)

# =========================
# 📷 VISION MODE
# =========================
st.markdown("---")
st.subheader("📷 Vision Mode (OCR)")

run = st.checkbox("Start Camera")

if run:
    cap = cv2.VideoCapture(0)
    frame_box = st.empty()

    while run:
        ret, frame = cap.read()
        if not ret:
            break

        frame_box.image(frame, channels="BGR")

        detected = vision(frame)

        st.info(f"👁️ Detected: {detected}")

        speak(detected)

    cap.release()

# =========================
# 🧠 MEMORY VIEW
# =========================
st.markdown("---")
st.subheader("🧠 Memory (Conversation History)")
# =========================
# 📷 OCR UPLOAD MODE (NEW)
# =========================
import numpy as np
from PIL import Image
import fitz  # PyMuPDF

st.markdown("---")
st.subheader("📁 OCR Upload Mode (Images + PDF)")

uploaded_file = st.file_uploader("Upload Image or PDF", type=["png", "jpg", "jpeg", "pdf"])

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

if uploaded_file is not None:

    file_type = uploaded_file.type

    # IMAGE OCR
    if "image" in file_type:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        extracted_text = extract_text_from_image(image)

        st.success("📝 Extracted Text:")
        st.write(extracted_text)

        speak(extracted_text)

    # PDF OCR
    elif "pdf" in file_type:
        st.info("Processing PDF...")

        extracted_text = extract_text_from_pdf(uploaded_file)

        st.success("📝 Extracted Text from PDF:")
        st.write(extracted_text)

        speak(extracted_text)