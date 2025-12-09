"""
Simplified OCR processor that prioritizes EasyOCR for handwritten text
"""
from typing import Union, List
import io

# Try to import dependencies
try:
    from PIL import Image, ImageEnhance, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

try:
    import pytesseract
    import os
    import platform
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


class SimpleOCR:
    """Simple OCR processor with enhanced preprocessing for better accuracy"""
    
    def __init__(self):
        self.easyocr_reader = None
        
        # Initialize EasyOCR if available
        if EASYOCR_AVAILABLE:
            try:
                # Use better parameters for handwritten text
                self.easyocr_reader = easyocr.Reader(['en'], gpu=False)
            except Exception:
                self.easyocr_reader = None
        
        # Setup Tesseract path if on Windows
        if TESSERACT_AVAILABLE and platform.system() == "Windows":
            self._setup_tesseract_path()
    
    def _setup_tesseract_path(self):
        """Setup Tesseract path for Windows"""
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME', '')),
            r"C:\Tesseract-OCR\tesseract.exe",
        ]
        
        for path in possible_paths:
            if os.path.isfile(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break
    
    def enhance_image(self, image: "Image.Image") -> "Image.Image":
        """
        Enhance image for better OCR accuracy
        """
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if image is too small (OCR works better with larger images)
        width, height = image.size
        if width < 1000 or height < 1000:
            scale_factor = max(1000 / width, 1000 / height)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)
        
        # Convert to grayscale for better text recognition
        image = image.convert('L')
        
        # Apply threshold to make text clearer
        if CV2_AVAILABLE:
            # Convert PIL to CV2
            img_array = np.array(image)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(img_array, (1, 1), 0)
            
            # Apply adaptive threshold
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Convert back to PIL
            image = Image.fromarray(thresh)
        
        return image
    
    def extract_text(self, image_input: Union[bytes, "Image.Image"]) -> str:
        """
        Extract text from image using available OCR engines with enhanced preprocessing
        """
        if not PIL_AVAILABLE:
            raise RuntimeError("PIL (Pillow) required. Install with: pip install pillow")
        
        # Convert bytes to PIL Image if needed
        if isinstance(image_input, bytes):
            image = Image.open(io.BytesIO(image_input))
        else:
            image = image_input
        
        # Enhance image for better OCR
        enhanced_image = self.enhance_image(image)
        
        # Try EasyOCR first with multiple configurations
        if self.easyocr_reader is not None:
            try:
                # Try different EasyOCR parameters for better accuracy
                
                # Method 1: Default paragraph mode
                results1 = self.easyocr_reader.readtext(
                    np.array(enhanced_image), 
                    paragraph=True,
                    width_ths=0.7,
                    height_ths=0.7
                )
                
                # Method 2: Without paragraph mode for individual words
                results2 = self.easyocr_reader.readtext(
                    np.array(enhanced_image),
                    paragraph=False,
                    width_ths=0.7,
                    height_ths=0.7
                )
                
                # Combine results and choose the best one
                text1 = self._process_easyocr_results(results1)
                text2 = self._process_easyocr_results(results2)
                
                # Choose the longer result (usually more complete)
                best_text = text1 if len(text1) > len(text2) else text2
                
                if best_text.strip():
                    return self._clean_text(best_text)
                    
            except Exception as e:
                pass  # Fall back to Tesseract
        
        # Fall back to Tesseract with multiple configurations
        if TESSERACT_AVAILABLE:
            try:
                # Convert enhanced image back to RGB for Tesseract
                if enhanced_image.mode == 'L':
                    enhanced_image = enhanced_image.convert('RGB')
                
                # Try different Tesseract configurations
                configs = [
                    '--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?;:()[]{}"\'-/\n ',
                    '--psm 4 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?;:()[]{}"\'-/\n ',
                    '--psm 3',
                    '--psm 6'
                ]
                
                best_result = ""
                for config in configs:
                    try:
                        text = pytesseract.image_to_string(enhanced_image, config=config)
                        if len(text.strip()) > len(best_result.strip()):
                            best_result = text
                    except:
                        continue
                
                if best_result.strip():
                    return self._clean_text(best_result)
                    
            except Exception as e:
                if self.easyocr_reader is not None:
                    return "Could not extract text. Please ensure image has clear, readable text."
                else:
                    raise RuntimeError(f"OCR failed: {str(e)}. Please install EasyOCR with: pip install easyocr")
        
        # No OCR engines available or both failed
        if self.easyocr_reader is not None:
            return "No text detected. Please check image quality and ensure text is clearly visible."
        else:
            raise RuntimeError("No OCR engines available. Install EasyOCR with: pip install easyocr")
    
    def _process_easyocr_results(self, results) -> str:
        """Process EasyOCR results and extract text"""
        text_parts = []
        
        for result in results:
            try:
                if len(result) == 3:
                    # Format: (bbox, text, confidence)
                    bbox, text, confidence = result
                    if confidence > 0.2:  # Lower threshold for handwritten text
                        text_parts.append(text)
                elif len(result) == 2:
                    # Format: (bbox, text)
                    bbox, text = result
                    text_parts.append(text)
                else:
                    # Unknown format
                    if isinstance(result, (list, tuple)) and len(result) > 1:
                        text_parts.append(str(result[1]))
            except:
                continue
        
        return ' '.join(text_parts)
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        if not text:
            return ""
        
        # Remove excessive whitespace and empty lines
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            cleaned_line = ' '.join(line.split())
            if cleaned_line.strip():
                cleaned_lines.append(cleaned_line)
        
        return '\n'.join(cleaned_lines)
    
    def process_multiple_images(self, images: List[Union[bytes, "Image.Image"]]) -> str:
        """Process multiple images"""
        all_text = []
        
        for i, image in enumerate(images):
            try:
                text = self.extract_text(image)
                if text.strip():
                    all_text.append(f"--- Page {i+1} ---\n{text}")
                else:
                    all_text.append(f"--- Page {i+1} ---\n[No text detected - please check image quality]")
            except Exception as e:
                all_text.append(f"--- Page {i+1} (Error) ---\nFailed to process: {str(e)}")
        
        return '\n\n'.join(all_text)
    
    def get_status(self) -> dict:
        """Get OCR engine status with actual testing"""
        status = {
            'easyocr_available': self.easyocr_reader is not None,
            'tesseract_available': False,
            'pil_available': PIL_AVAILABLE
        }
        
        # Test Tesseract actually works
        if TESSERACT_AVAILABLE:
            try:
                # Try to get version to verify it works
                pytesseract.get_tesseract_version()
                status['tesseract_available'] = True
            except Exception:
                # Tesseract not working properly
                status['tesseract_available'] = False
        
        return status
