import streamlit as st
import cv2
import numpy as np
import easyocr
import speech_recognition as sr
import pyttsx3
import threading
import time
import re

# -----------------------------
# TEXT TO SPEECH ENGINE
# -----------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run).start()

# -----------------------------
# SPEECH TO TEXT
# -----------------------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text.lower()
    except:
        return "sorry i could not understand"

# -----------------------------
# OCR
# -----------------------------
reader = easyocr.Reader(['en'])

def read_text(image):
    result = reader.readtext(image)
    text = " ".join([r[1] for r in result])
    return text if text else "No readable text found"

# -----------------------------
# AI BRAIN
# -----------------------------
def ai_brain(command):
    command = command.lower()

    if "navigate" in command:
        return "Moving forward. Slight obstacle on left. Turn right."

    elif "stop" in command:
        return "Stopping immediately. Safe position achieved."

    elif "read" in command:
        return "Switching to reading mode. Show document."

    elif "help" in command:
        return "I can help with navigation, reading, and camera analysis."

    elif "delhi" in command and "indore" in command:
        return "Route: Take NH52 via Jaipur. Approx 12 hours travel."

    else:
        return "Command not recognized. Try navigate, read, or help."

# -----------------------------
# CAMERA ANALYSIS
# -----------------------------
def analyze_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)

    if brightness < 50:
        return "⚠️ Low light detected. Turn on light."
    elif brightness > 200:
        return "Bright environment. Path likely clear."
    else:
        return "Normal environment. Minor obstacles possible."

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="AI Accessibility Agent", layout="wide")

st.title("♿ AI Accessibility Companion Agent (MVP)")
st.markdown("Voice + Vision + OCR Assistant")

mode = st.sidebar.selectbox("Choose Mode", [
    "🎤 Voice Mode",
    "📷 Camera Mode",
    "📖 OCR Reader",
    "🧭 Navigation Assistant"
])

# -----------------------------
# VOICE MODE
# -----------------------------
if mode == "🎤 Voice Mode":
    st.subheader("Voice Assistant")

    if st.button("Start Listening"):
        command = listen()
        st.write("🗣️ You said:", command)

        response = ai_brain(command)
        st.write("🤖 AI:", response)

        speak(response)

# -----------------------------
# CAMERA MODE
# -----------------------------
elif mode == "📷 Camera Mode":
    st.subheader("Live Camera Analysis")

    run = st.checkbox("Start Camera")
    cap = cv2.VideoCapture(0)

    while run:
        ret, frame = cap.read()
        if not ret:
            st.error("Camera not found")
            break

        st.image(frame, channels="BGR")

        msg = analyze_frame(frame)
        st.success(msg)

        speak(msg)
        time.sleep(2)

    cap.release()

# -----------------------------
# OCR MODE
# -----------------------------
elif mode == "📖 OCR Reader":
    st.subheader("Read Text from Image")

    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        st.image(img, channels="BGR")

        text = read_text(img)
        st.success("📄 Extracted Text:")
        st.write(text)

        speak(text)

# -----------------------------
# NAVIGATION MODE
# -----------------------------
elif mode == "🧭 Navigation Assistant":
    st.subheader("Smart Navigation Guide")

    user_input = st.text_input("Enter command (or speak in Voice Mode)")

    if st.button("Run Navigation"):
        response = ai_brain(user_input)
        st.success(response)
        speak(response)

# -----------------------------
st.markdown("---")
st.markdown("🔥 Built for Hackathon | AI Accessibility Companion MVP")