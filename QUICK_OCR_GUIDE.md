# Simple OCR Setup Guide

## Quick Installation

### For Windows (Recommended)

```cmd
install_ocr_windows.bat
```

### For Linux/macOS

```bash
pip install pillow easyocr
```

## What you get:

- ✅ **EasyOCR**: Best for handwritten text (recommended)
- ⚠️ **Tesseract**: Optional, better for printed text

## Usage:

1. Run: `streamlit run app.py`
2. Choose "📸 Upload Images"
3. Upload your handwritten essay images
4. Click "Extract Text from Images"
5. Review and edit the extracted text
6. Evaluate your essay!

## Troubleshooting:

- **No OCR available?** → Run `pip install easyocr`
- **Poor text recognition?** → Use better lighting, clearer handwriting
- **First run slow?** → EasyOCR downloads models (~100MB), normal behavior

## Tips for best results:

- Use good lighting
- Write clearly
- Use dark ink on white paper
- Keep images horizontal
- Use high resolution (phone camera is fine)

That's it! The app handles everything else automatically.
