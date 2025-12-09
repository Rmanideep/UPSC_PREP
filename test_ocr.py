"""
Test script for OCR functionality
"""
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.ocr import OCRProcessor, OCREngine
    print("✅ OCR module imported successfully")
except ImportError as e:
    print(f"❌ Failed to import OCR module: {e}")
    sys.exit(1)

def test_ocr_engines():
    """Test available OCR engines"""
    print("\n🔍 Testing OCR Engines...")
    
    # Test EasyOCR
    try:
        processor = OCRProcessor(engine=OCREngine.EASYOCR)
        print("✅ EasyOCR: Available")
    except Exception as e:
        print(f"❌ EasyOCR: {e}")
    
    # Test Tesseract
    try:
        processor = OCRProcessor(engine=OCREngine.TESSERACT)
        print("✅ Tesseract: Available")
    except Exception as e:
        print(f"❌ Tesseract: {e}")

def test_image_processing():
    """Test image processing capabilities"""
    print("\n🖼️ Testing Image Processing...")
    
    try:
        import cv2
        import numpy as np
        from PIL import Image
        
        # Create a simple test image with text
        test_image = np.ones((200, 600, 3), dtype=np.uint8) * 255
        cv2.putText(test_image, "This is a test essay.", (50, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Test preprocessing
        processor = OCRProcessor(engine=OCREngine.EASYOCR)
        processed = processor.preprocess_image(test_image)
        
        print("✅ Image preprocessing: Working")
        
        # Test text extraction (if EasyOCR is available)
        try:
            text = processor.extract_text_easyocr(processed)
            print(f"✅ Text extraction: '{text[:50]}...' (EasyOCR)")
        except:
            print("⚠️ EasyOCR text extraction: Not available")
        
        # Test with Tesseract if available
        try:
            processor_tess = OCRProcessor(engine=OCREngine.TESSERACT)
            text = processor_tess.extract_text_tesseract(processed)
            print(f"✅ Text extraction: '{text[:50]}...' (Tesseract)")
        except:
            print("⚠️ Tesseract text extraction: Not available")
            
    except Exception as e:
        print(f"❌ Image processing test failed: {e}")

def main():
    print("🧪 UPSC Essay Evaluator - OCR Test Suite")
    print("=" * 50)
    
    test_ocr_engines()
    test_image_processing()
    
    print("\n📋 Test Summary:")
    print("- If EasyOCR is available: Ready for handwritten text OCR")
    print("- If Tesseract is available: Ready for printed text OCR")
    print("- If both fail: Check installation requirements")
    print("\nFor setup help, see OCR_SETUP.md")

if __name__ == "__main__":
    main()
