# OCR Setup Instructions for UPSC Essay Evaluator

This document provides instructions for setting up OCR functionality in the UPSC Essay Evaluator.

## Prerequisites

### For Tesseract OCR

1. **Windows:**

   - Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install Tesseract and note the installation path (usually `C:\Program Files\Tesseract-OCR\tesseract.exe`)
   - Add Tesseract to your system PATH or set the path in your code

2. **macOS:**

   ```bash
   brew install tesseract
   ```

3. **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt update
   sudo apt install tesseract-ocr
   ```

### For EasyOCR (Recommended for handwritten text)

EasyOCR will be installed automatically with pip, but requires:

- Python 3.6+
- PyTorch (will be installed automatically)

## Installation

1. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **For Windows users with Tesseract:**
   If Tesseract is not in your PATH, you may need to set the path in your code:
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

## Usage

1. **Start the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

2. **Upload images:**
   - Select "📸 Upload Images" as input method
   - Upload JPG, PNG, or JPEG images of handwritten essays
   - Choose OCR engine (EasyOCR recommended for handwriting)
   - Click "Extract Text from Images"
   - Review and edit extracted text if needed
   - Proceed with essay evaluation

## OCR Engine Comparison

### EasyOCR (Recommended)

- **Pros:** Better accuracy for handwritten text, supports multiple languages, no additional setup
- **Cons:** Slower processing, larger memory usage
- **Best for:** Handwritten essays, mixed text types

### Tesseract

- **Pros:** Faster processing, smaller memory footprint, highly configurable
- **Cons:** Less accurate for handwritten text, requires separate installation
- **Best for:** Printed text, typed documents

## Tips for Better OCR Results

1. **Image Quality:**

   - Use good lighting without shadows
   - Ensure high resolution (at least 300 DPI)
   - Keep the camera steady to avoid blur

2. **Handwriting:**

   - Write clearly and legibly
   - Use dark ink on light paper
   - Leave adequate spacing between lines
   - Avoid writing at angles

3. **Camera/Scanner Settings:**
   - Capture the entire page
   - Ensure the text is horizontal
   - Use maximum resolution available
   - Save in high-quality format (PNG preferred)

## Troubleshooting

### Common Issues:

1. **"Tesseract not found" error:**

   - Ensure Tesseract is installed and in PATH
   - Set the tesseract_cmd path manually if needed

2. **Poor OCR accuracy:**

   - Try different OCR engine
   - Improve image quality (lighting, resolution, clarity)
   - Enable image preprocessing in settings

3. **EasyOCR initialization errors:**

   - Ensure stable internet connection for first-time model download
   - Check available disk space (models are ~100MB)

4. **Memory issues:**
   - Close other applications
   - Try processing images one at a time
   - Use Tesseract for lower memory usage

### Performance Optimization:

1. **For better speed:**

   - Use Tesseract OCR engine
   - Disable image preprocessing if not needed
   - Process smaller image files

2. **For better accuracy:**
   - Use EasyOCR engine
   - Enable image preprocessing
   - Ensure high-quality input images
   - Manually review and edit extracted text

## File Size Limits

- Maximum file size per image: 200MB (Streamlit default)
- Recommended image size: 2-10MB for best balance of quality and processing speed
- For large files, consider compressing images while maintaining readability
