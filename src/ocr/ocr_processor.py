from enum import Enum
from typing import Optional, Union
import io

# Try to import OCR dependencies
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False


class OCREngine(Enum):
    """Available OCR engines"""
    TESSERACT = "tesseract"
    EASYOCR = "easyocr"


class OCRProcessor:
    """
    OCR processor for extracting text from images of handwritten essays
    """
    
    def __init__(self, engine: OCREngine = OCREngine.EASYOCR):
        """
        Initialize OCR processor
        
        Args:
            engine: OCR engine to use (TESSERACT or EASYOCR)
        """
        self.engine = engine
        self._easyocr_reader = None
        
        # Check dependencies
        if not self._check_dependencies():
            raise RuntimeError(
                "OCR dependencies not installed. Please run: pip install pillow opencv-python pytesseract easyocr numpy"
            )
        
        # Initialize EasyOCR reader if needed and available
        if engine == OCREngine.EASYOCR:
            if not EASYOCR_AVAILABLE:
                raise RuntimeError(
                    "EasyOCR not available. Install with: pip install easyocr"
                )
            self._init_easyocr()
        elif engine == OCREngine.TESSERACT:
            if not TESSERACT_AVAILABLE:
                raise RuntimeError(
                    "Tesseract not available. Install with: pip install pytesseract"
                )
    
    def _check_dependencies(self) -> bool:
        """Check if minimum dependencies are available"""
        return PIL_AVAILABLE and NUMPY_AVAILABLE
    
    def _init_easyocr(self):
        """Initialize EasyOCR reader"""
        try:
            if EASYOCR_AVAILABLE:
                self._easyocr_reader = easyocr.Reader(['en'])
            else:
                raise RuntimeError("EasyOCR not available")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize EasyOCR: {str(e)}")
    
    def preprocess_image(self, image: Union["np.ndarray", "Image.Image"]) -> "np.ndarray":
        """
        Preprocess image for better OCR results
        
        Args:
            image: Input image (PIL Image or numpy array)
            
        Returns:
            Preprocessed image as numpy array
        """
        if not CV2_AVAILABLE or not NUMPY_AVAILABLE:
            raise RuntimeError("OpenCV and NumPy required for image preprocessing. Install with: pip install opencv-python numpy")
        
        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image.copy()
        
        # Apply noise reduction
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Apply adaptive thresholding for better text contrast
        adaptive_thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Optional: Apply morphological operations to clean up the image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        cleaned = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def extract_text_tesseract(self, image: "np.ndarray") -> str:
        """
        Extract text using Tesseract OCR
        
        Args:
            image: Preprocessed image
            
        Returns:
            Extracted text
        """
        if not TESSERACT_AVAILABLE:
            raise RuntimeError("Tesseract not available. Install with: pip install pytesseract")
        
        try:
            # Try to set Tesseract path if it's not in PATH (Windows)
            import platform
            if platform.system() == "Windows":
                self._setup_tesseract_path()
            
            # Configure Tesseract for handwritten text
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?;:()[]{}"\'-/\n '
            
            text = pytesseract.image_to_string(image, config=custom_config)
            return text.strip()
        except Exception as e:
            raise RuntimeError(f"Tesseract OCR failed: {str(e)}. Please install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki")
    
    def _setup_tesseract_path(self):
        """Setup Tesseract path for Windows if not in PATH"""
        import os
        
        # Common Tesseract installation paths on Windows
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME', '')),
            r"C:\Tesseract-OCR\tesseract.exe",
        ]
        
        for path in possible_paths:
            if os.path.isfile(path):
                pytesseract.pytesseract.tesseract_cmd = path
                return
        
        # If not found, let pytesseract handle the error
    
    def extract_text_easyocr(self, image: "np.ndarray") -> str:
        """
        Extract text using EasyOCR
        
        Args:
            image: Preprocessed image
            
        Returns:
            Extracted text
        """
        if not EASYOCR_AVAILABLE:
            raise RuntimeError("EasyOCR not available. Install with: pip install easyocr")
        
        try:
            if self._easyocr_reader is None:
                self._init_easyocr()
            
            # Extract text with EasyOCR
            results = self._easyocr_reader.readtext(image, paragraph=True)
            
            # Combine all detected text
            extracted_text = []
            for (bbox, text, confidence) in results:
                # Filter out low confidence detections
                if confidence > 0.3:
                    extracted_text.append(text)
            
            return ' '.join(extracted_text)
        except Exception as e:
            raise RuntimeError(f"EasyOCR failed: {str(e)}")
    
    def process_image(self, image_input: Union[bytes, "Image.Image", "np.ndarray"], 
                     preprocess: bool = True) -> str:
        """
        Process image and extract text
        
        Args:
            image_input: Image input (bytes, PIL Image, or numpy array)
            preprocess: Whether to apply preprocessing
            
        Returns:
            Extracted text
        """
        if not PIL_AVAILABLE:
            raise RuntimeError("PIL (Pillow) required for image processing. Install with: pip install pillow")
        
        try:
            # Handle different input types
            if isinstance(image_input, bytes):
                image = Image.open(io.BytesIO(image_input))
            elif isinstance(image_input, Image.Image):
                image = image_input
            elif NUMPY_AVAILABLE and isinstance(image_input, np.ndarray):
                image = Image.fromarray(image_input)
            else:
                raise ValueError("Unsupported image input type or NumPy not available")
            
            # Convert to numpy array for processing
            if not NUMPY_AVAILABLE:
                raise RuntimeError("NumPy required for image processing. Install with: pip install numpy")
            
            img_array = np.array(image)
            
            # Preprocess image if requested
            if preprocess:
                img_array = self.preprocess_image(img_array)
            
            # Extract text based on selected engine
            if self.engine == OCREngine.TESSERACT:
                text = self.extract_text_tesseract(img_array)
            elif self.engine == OCREngine.EASYOCR:
                text = self.extract_text_easyocr(img_array)
            else:
                raise ValueError(f"Unsupported OCR engine: {self.engine}")
            
            # Clean up the extracted text
            text = self._clean_text(text)
            
            return text
            
        except Exception as e:
            raise RuntimeError(f"Image processing failed: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """
        Clean up extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove extra spaces
            cleaned_line = ' '.join(line.split())
            if cleaned_line.strip():  # Only add non-empty lines
                cleaned_lines.append(cleaned_line)
        
        # Join lines with single newlines
        cleaned_text = '\n'.join(cleaned_lines)
        
        return cleaned_text
    
    def process_multiple_images(self, images: list, preprocess: bool = True) -> str:
        """
        Process multiple images and combine extracted text
        
        Args:
            images: List of images (any supported format)
            preprocess: Whether to apply preprocessing
            
        Returns:
            Combined extracted text
        """
        all_text = []
        
        for i, image in enumerate(images):
            try:
                text = self.process_image(image, preprocess)
                if text.strip():
                    all_text.append(f"--- Page {i+1} ---\n{text}")
            except Exception as e:
                all_text.append(f"--- Page {i+1} (Error) ---\nFailed to process: {str(e)}")
        
        return '\n\n'.join(all_text)


def get_available_engines() -> list:
    """
    Get list of available OCR engines
    
    Returns:
        List of available OCR engines
    """
    available = []
    
    # Check Tesseract
    if TESSERACT_AVAILABLE:
        try:
            pytesseract.get_tesseract_version()
            available.append(OCREngine.TESSERACT)
        except:
            pass
    
    # Check EasyOCR
    if EASYOCR_AVAILABLE:
        available.append(OCREngine.EASYOCR)
    
    return available


def check_ocr_dependencies() -> dict:
    """
    Check which OCR dependencies are available
    
    Returns:
        Dictionary with availability status
    """
    return {
        'pillow': PIL_AVAILABLE,
        'opencv': CV2_AVAILABLE,
        'numpy': NUMPY_AVAILABLE,
        'tesseract': TESSERACT_AVAILABLE,
        'easyocr': EASYOCR_AVAILABLE
    }
