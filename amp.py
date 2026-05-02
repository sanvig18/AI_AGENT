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