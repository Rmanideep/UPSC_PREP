@echo off
echo ============================================
echo UPSC Essay Evaluator OCR Setup Script
echo ============================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Checking OCR engines...

echo.
echo Testing EasyOCR installation...
python -c "import easyocr; print('EasyOCR: OK')" 2>nul || echo "EasyOCR: Failed to import"

echo.
echo Testing Tesseract installation...
python -c "import pytesseract; pytesseract.get_tesseract_version(); print('Tesseract: OK')" 2>nul || echo "Tesseract: Not found or not in PATH"

echo.
echo ============================================
echo Setup Summary:
echo ============================================
echo - Python dependencies installed
echo - OCR engines checked
echo.
echo If Tesseract is not found:
echo 1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
echo 2. Install and add to PATH
echo 3. Or use EasyOCR only (recommended for handwriting)
echo.
echo To start the application:
echo streamlit run app.py
echo.
pause
