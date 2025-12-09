#!/bin/bash

echo "============================================"
echo "UPSC Essay Evaluator OCR Setup Script"
echo "============================================"
echo

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo
echo "Checking OCR engines..."

echo
echo "Testing EasyOCR installation..."
python -c "import easyocr; print('EasyOCR: OK')" 2>/dev/null || echo "EasyOCR: Failed to import"

echo
echo "Testing Tesseract installation..."
python -c "import pytesseract; pytesseract.get_tesseract_version(); print('Tesseract: OK')" 2>/dev/null || echo "Tesseract: Not found"

echo
echo "============================================"
echo "Setup Summary:"
echo "============================================"
echo "- Python dependencies installed"
echo "- OCR engines checked"
echo

if ! command -v tesseract &> /dev/null; then
    echo "Tesseract not found. To install:"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS: brew install tesseract"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Linux: sudo apt install tesseract-ocr"
    fi
    echo "Or use EasyOCR only (recommended for handwriting)"
fi

echo
echo "To start the application:"
echo "streamlit run app.py"
echo
