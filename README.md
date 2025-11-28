# 🧠 NeuroReader: AI Text Scanner & Speaker

NeuroReader is an Intelligent Document Processing app built with Python. It allows users to upload images or use their webcam to scan text, displays the text on screen, and reads it aloud using AI voice generation.

## 🚀 Features
- **OCR (Optical Character Recognition):** Extracts text from images using Tesseract.
- **Computer Vision:** Pre-processes images (thresholding/blurring) for higher accuracy.
- **Text-to-Speech:** Converts recognized text into MP3 audio.
- **Dual Mode:** Works with file uploads and live webcam feeds.

## 🛠️ Tech Stack
- **Python**
- **Streamlit** (Frontend)
- **OpenCV** (Image Processing)
- **Tesseract** (OCR Engine)
- **gTTS** (Google Text-to-Speech)

## 📦 How to Run
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
