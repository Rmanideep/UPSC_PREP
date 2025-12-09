@echo off
echo ============================================
echo Installing OCR Dependencies for Windows
echo ============================================
echo.

echo Step 1: Installing Python packages...
pip install pillow opencv-python pytesseract easyocr numpy

echo.
echo Step 2: Checking Tesseract installation...
tesseract --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo ✅ Tesseract is already installed and in PATH
) else (
    echo ❌ Tesseract not found in PATH
    echo.
    echo Downloading and installing Tesseract...
    echo Please install Tesseract manually from:
    echo https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    echo After installation, add Tesseract to your PATH or
    echo the app will automatically try to find it.
    echo.
    echo Common installation paths:
    echo - C:\Program Files\Tesseract-OCR\tesseract.exe
    echo - C:\Users\%USERNAME%\AppData\Local\Programs\Tesseract-OCR\tesseract.exe
)

echo.
echo Step 3: Testing EasyOCR (recommended for handwritten text)...
python -c "import easyocr; print('✅ EasyOCR installed successfully')" 2>nul || echo "❌ EasyOCR installation failed"

echo.
echo Step 4: Testing image processing libraries...
python -c "import cv2; print('✅ OpenCV installed successfully')" 2>nul || echo "❌ OpenCV installation failed"
python -c "import numpy; print('✅ NumPy installed successfully')" 2>nul || echo "❌ NumPy installation failed"

echo.
echo ============================================
echo Installation Summary
echo ============================================
echo.
echo ✅ RECOMMENDED SETUP:
echo    - EasyOCR is the best choice for handwritten text
echo    - It works without additional configuration
echo    - Provides good accuracy for student essays
echo.
echo ⚙️ OPTIONAL (Tesseract):
echo    - Better for printed text
echo    - Requires manual installation from link above
echo    - Used as fallback if EasyOCR fails
echo.
echo 🚀 PERFORMANCE TIPS:
echo    - Use high-resolution images (at least 2MP)
echo    - Ensure good lighting and contrast
echo    - Keep handwriting clear and dark
echo    - Avoid shadows and glare
echo.
echo To test the app: streamlit run app.py
echo.
pause
