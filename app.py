import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
import os

# Set path for Linux (Colab default)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# --- PAGE CONFIG ---
st.set_page_config(page_title="NeuroReader Pro", layout="centered")
st.title("🧠 NeuroReader: AI Text Scanner")
st.markdown("Upload an image or use the camera to extract and read text.")

# --- FUNCTIONS ---
def preprocess_image(image):
    """
    Cleans the image to make it easier for AI to read.
    1. Grayscale
    2. Blur (remove noise)
    3. Threshold (make text strict Black & White)
    """
    # Convert PIL Image to OpenCV format
    img_array = np.array(image)
    
    # Convert to Grayscale
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian Blur (removes grainy noise)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply Otsu's Thresholding (separates text from background)
    # This creates a high-contrast Black & White image
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh

def text_to_speech(text):
    """Generates MP3 from text using Google TTS"""
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        filename = "audio_output.mp3"
        tts.save(filename)
        return filename
    except Exception as e:
        st.error(f"Audio Error: {e}")
        return None

# --- SIDEBAR OPTIONS ---
st.sidebar.header("Settings")
source_radio = st.sidebar.radio("Select Source", ["📷 Camera", "📁 Upload Image"])
preprocess_toggle = st.sidebar.checkbox("Show AI Vision (Debug Mode)", value=False)

# --- MAIN LOGIC ---
image_input = None

if source_radio == "📁 Upload Image":
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'png', 'jpeg'])
    if uploaded_file is not None:
        image_input = Image.open(uploaded_file)

elif source_radio == "📷 Camera":
    camera_file = st.camera_input("Take a picture")
    if camera_file is not None:
        image_input = Image.open(camera_file)

# --- PROCESSING ---
if image_input is not None:
    # 1. Show Original
    st.image(image_input, caption="Original Image", use_column_width=True)
    
    # 2. Pre-process (The "AI Vision")
    processed_img = preprocess_image(image_input)
    
    if preprocess_toggle:
        st.image(processed_img, caption="What the AI sees (Pre-processed)", use_column_width=True, clamp=True)

    # 3. Extract Text Button
    if st.button("🔍 Scan & Read Text", type="primary"):
        with st.spinner("Analyzing image patterns..."):
            # Run Tesseract on the PROCESSED image, not the original
            # psm 6 = Assume a single uniform block of text
            custom_config = r'--oem 3 --psm 6'
            extracted_text = pytesseract.image_to_string(processed_img, config=custom_config)
            
            if extracted_text.strip():
                st.success("Text Found!")
                st.text_area("Extracted Text:", extracted_text, height=200)
                
                # 4. Generate Audio
                st.markdown("---")
                st.subheader("🔊 Audio Output")
                with st.spinner("Generating audio voiceover..."):
                    audio_file = text_to_speech(extracted_text)
                    if audio_file:
                        st.audio(audio_file, format="audio/mp3")
            else:
                st.warning("No text detected. Try a clearer image or check 'Show AI Vision' to see if the text is visible.")
