import streamlit as st

if "page" not in st.session_state:
    st.session_state.page = "home"
    page = st.sidebar.selectbox(
    "Navigate",
    ["Home", "MVP", "Voice", "Camera"]
)
    if page == "Home":
    st.title("🏠 Homepage")
    st.write("Welcome to AI Accessibility Agent")

elif page == "MVP":
    st.title("🚀 MVP Dashboard")
    st.write("Core AI features here")

elif page == "Voice":
    st.title("🎤 Voice Mode")

elif page == "Camera":
    st.title("📷 Camera Mode")
    def home_page():
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.title("♿ AI Accessibility Assistant")
    st.subheader("Voice • Vision • Memory • Intelligence")

    st.markdown("""
    ### 👋 Welcome to your AI Companion

    This assistant is designed to help users with accessibility needs using AI-powered tools.

    ---
    """)

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### 🎤 Voice AI")
        st.write("Speak naturally and get instant AI responses.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### 📷 Vision AI")
        st.write("Read text from images using OCR technology.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### 🧠 Memory AI")
        st.write("Remembers conversations for personalized help.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("""
    ## 🚀 Why this stands out in hackathons

    ✔ Real-time voice interaction  
    ✔ Vision-based accessibility  
    ✔ Persistent AI memory  
    ✔ Clean modern UI (Glassmorphism)  
    ✔ Designed for real-world disability assistance  

    ---
    ### 🧭 Use sidebar to navigate features
    """)
    st.markdown("</div>", unsafe_allow_html=True)