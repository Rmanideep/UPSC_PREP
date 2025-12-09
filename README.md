# UPSC Essay Evaluator with OCR

A Streamlit web application that evaluates UPSC essays using LangGraph and OpenAI's language models. The app provides detailed feedback on language quality, depth of analysis, and clarity of thought. **NEW: Now supports OCR for handwritten essay images!**

## Features

- **📝 Text Input**: Type or paste essays directly
- **📸 OCR Support**: Upload images of handwritten essays for automatic text extraction
- **⚡ Parallel Evaluation**: Uses LangGraph to evaluate essays on multiple criteria simultaneously
- **📊 Detailed Feedback**: Provides specific feedback for language, analysis, and clarity
- **🎨 Interactive UI**: Clean and user-friendly Streamlit interface
- **💾 Downloadable Reports**: Export evaluation results as text files
- **🏗️ Modular Architecture**: Well-structured codebase with separate modules

## OCR Capabilities

- **Multiple OCR Engines**: Choose between EasyOCR (better for handwriting) and Tesseract (faster)
- **Image Preprocessing**: Automatic image enhancement for better text recognition
- **Multi-page Support**: Upload multiple images for lengthy essays
- **Format Support**: JPG, PNG, JPEG image formats
- **Real-time Preview**: See uploaded images before text extraction

## Project Structure

```
upsc_essay_app/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies (including OCR)
├── setup_ocr.bat              # Windows setup script
├── setup_ocr.sh               # Linux/Mac setup script
├── OCR_SETUP.md               # Detailed OCR setup instructions
├── README.md                  # This file
└── src/
    ├── __init__.py
    ├── models/
    │   ├── __init__.py
    │   ├── schemas.py         # Pydantic models and TypedDict definitions
    │   └── llm_config.py      # LLM configuration and initialization
    ├── ocr/                   # NEW: OCR functionality
    │   ├── __init__.py
    │   └── ocr_processor.py   # OCR processing with multiple engines
    ├── evaluators/
    │   ├── __init__.py
    │   ├── language_evaluator.py    # Language quality evaluation
    │   ├── analysis_evaluator.py    # Depth of analysis evaluation
    │   ├── clarity_evaluator.py     # Clarity of thought evaluation
    │   └── final_evaluator.py       # Final evaluation and summary
    └── workflow/
        ├── __init__.py
        └── essay_workflow.py         # LangGraph workflow definition
```

## Installation

### Quick Setup (Recommended)

**Windows:**

```bash
setup_ocr.bat
```

**Linux/Mac:**

```bash
chmod +x setup_ocr.sh
./setup_ocr.sh
```

### Manual Installation

1. **Clone or download the project**

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Install OCR engines**:

   **For Tesseract (Windows):**

   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install and add to system PATH

   **For Tesseract (macOS):**

   ```bash
   brew install tesseract
   ```

   **For Tesseract (Linux):**

   ```bash
   sudo apt update
   sudo apt install tesseract-ocr
   ```

   **EasyOCR** will be installed automatically with pip requirements.

4. **Set up environment variables**:

   - Copy `.env.example` to `.env`
   - Add your OpenRouter API key to the `.env` file:
     ```
     OPENROUTER_API_KEY=your_openrouter_api_key_here
     ```

5. **Run the application**:

   ```bash
   streamlit run app.py
   ```

   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

6. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Usage

### Text Input Method

1. **Select "✍️ Type/Paste Text"**
2. **Enter your essay** in the text area
3. **Click 'Evaluate Essay'** to start the evaluation

### Image Upload Method (NEW!)

1. **Select "📸 Upload Images"**
2. **Upload one or more images** of your handwritten essay (JPG, PNG, JPEG)
3. **Preview uploaded images** in the interface
4. **Click 'Extract Text from Images'** to process with OCR
5. **Review and edit** the extracted text if needed
6. **Click 'Evaluate Essay'** to start the evaluation

### Review Results

- **Overall score** (average of all criteria)
- **Individual scores** for each criterion
- **Detailed feedback** for each aspect
- **Overall summary**
- **Download the report** if needed

## OCR Tips for Best Results

### Image Quality

- Use good lighting without shadows
- Ensure high resolution (at least 300 DPI)
- Keep the camera steady to avoid blur
- Capture the entire page

### Handwriting

- Write clearly and legibly
- Use dark ink on light paper
- Leave adequate spacing between lines
- Avoid writing at angles

### OCR Engine Selection

- **EasyOCR**: Better for handwritten text, more accurate but slower
- **Tesseract**: Faster processing, better for printed text

## Evaluation Criteria

- **Language Quality**: Grammar, vocabulary, sentence structure, and overall writing quality
- **Depth of Analysis**: Critical thinking, use of evidence, strength of arguments
- **Clarity of Thought**: Logical flow, coherence, and organization of ideas

## Configuration

The app uses OpenAI's language models through the LangChain library. You can modify the model settings in `src/models/llm_config.py`:

- Model name
- Temperature
- Other parameters

## Dependencies

### Core Application

- **Streamlit**: Web application framework
- **LangGraph**: Workflow orchestration
- **LangChain**: LLM integration
- **OpenAI**: Language model API
- **Pydantic**: Data validation
- **python-dotenv**: Environment variable management

### OCR Functionality

- **Pillow**: Image processing
- **OpenCV**: Advanced image preprocessing
- **pytesseract**: Tesseract OCR engine wrapper
- **easyocr**: Deep learning-based OCR engine
- **numpy**: Numerical operations for image processing

## Troubleshooting

### OCR Issues

- **"Tesseract not found"**: Ensure Tesseract is installed and in PATH
- **Poor OCR accuracy**: Try different OCR engine, improve image quality
- **Memory issues**: Close other applications, try processing one image at a time

### Common Solutions

- Check image quality (lighting, resolution, clarity)
- Use EasyOCR for handwritten text
- Enable image preprocessing in settings
- Manually review and edit extracted text

For detailed OCR setup instructions, see `OCR_SETUP.md`.

## Contributing

Feel free to submit issues and pull requests to improve the application.

## License

This project is open source and available under the MIT License.
