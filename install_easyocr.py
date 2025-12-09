"""
Simple EasyOCR installer for UPSC Essay Evaluator
"""
import subprocess
import sys

def install_easyocr():
    """Install EasyOCR using pip"""
    try:
        print("Installing EasyOCR...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "easyocr"])
        print("✅ EasyOCR installed successfully!")
        print("Please restart the Streamlit app to use OCR functionality.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install EasyOCR: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    install_easyocr()
