import streamlit as st
import sys
import os
from PIL import Image

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.workflow import evaluate_essay
from src.models import EvaluationResult

# Try to import OCR functionality
try:
    from src.ocr.simple_ocr import SimpleOCR
    OCR_AVAILABLE = True
    # Test OCR initialization
    _test_ocr = SimpleOCR()
    OCR_STATUS = _test_ocr.get_status()
except ImportError as e:
    OCR_AVAILABLE = False
    OCR_STATUS = {}
    print(f"OCR functionality not available: {e}")

# Set page config
st.set_page_config(
    page_title="UPSC Essay Evaluator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 30px;
    }
.score-box {
    background-color: #f0f2f6;
    border-radius: 12px;
    padding: 20px;
    margin: 16px 0;
    border-left: 5px solid #2E86AB;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05); /* Optional: soft shadow for depth */
    font-family: sans-serif; /* Optional: improves consistency with other cards */
    color: #333; /* Improves text visibility */
}

    .feedback-section {
        background-color: #c9a25d;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #ffffff; /* Light text for better readability on gradient */
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    margin: 16px 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Optional: adds depth */
    font-family: sans-serif; /* Ensures cleaner appearance */
    transition: transform 0.2s ease; /* Optional: subtle hover effect */
}

.metric-card:hover {
    transform: translateY(-2px);
}

</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🎓 UPSC Essay Evaluator</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🔑 API Configuration")
        api_key = st.text_input(
            "OpenRouter API Key:",
            type="password",
            placeholder="Enter your OpenRouter API key",
            help="Get your API key from https://openrouter.ai/keys"
        )
        
        st.markdown("---")
        
        # OCR Settings (only show if OCR is available)
        if OCR_AVAILABLE:
            st.header("🔧 OCR Settings")
            
            # Show OCR status
            if OCR_STATUS.get('easyocr_available', False):
                st.success("✅ EasyOCR: Ready (Recommended for handwriting)")
            else:
                st.warning("⚠️ EasyOCR: Not available")
                st.info("💡 Install EasyOCR for best handwriting recognition:")
                st.code("pip install easyocr")
            
            if OCR_STATUS.get('tesseract_available', False):
                st.success("✅ Tesseract: Ready")
            else:
                st.warning("⚠️ Tesseract: Not available or not in PATH")
            
            if not any(OCR_STATUS.values()):
                st.error("❌ No OCR engines available")
                st.markdown("**Quick fix (Recommended):**")
                st.code("pip install easyocr")
                st.markdown("**Or run the installer:**")
                st.code("install_ocr_windows.bat")
            elif not OCR_STATUS.get('easyocr_available', False):
                st.warning("💡 For best handwriting recognition, install EasyOCR:")
                st.code("pip install easyocr")
        else:
            st.header("📸 OCR Not Available")
            st.warning("⚠️ OCR dependencies not installed")
            st.markdown("**To enable OCR functionality:**")
            st.code("pip install pillow easyocr")
            st.markdown("**Or run the installer:**")
            st.code("install_ocr_windows.bat")
            
        st.markdown("---")
        
        st.header("📋 Instructions")
        if OCR_AVAILABLE and any(OCR_STATUS.values()):
            st.markdown("""
            1. **Enter your OpenRouter API key** above
            2. **Choose input method:**
               - Type/paste your essay directly, OR
               - Upload image(s) of handwritten essay
            3. **Click 'Evaluate Essay'** to get feedback
            4. **Review the results** across three criteria:
               - 🗣️ Language Quality
               - 🔍 Depth of Analysis  
               - 💭 Clarity of Thought
            5. **Get overall feedback** and average score
            """)
        else:
            st.markdown("""
            1. **Enter your OpenRouter API key** above
            2. **Type/paste your essay** in the text area
            3. **Click 'Evaluate Essay'** to get feedback
            4. **Review the results** across three criteria:
               - 🗣️ Language Quality
               - 🔍 Depth of Analysis  
               - 💭 Clarity of Thought
            5. **Get overall feedback** and average score
            """)
        
        st.header("📊 Evaluation Criteria")
        st.markdown("""
        - **Language Quality**: Grammar, vocabulary, sentence structure
        - **Depth of Analysis**: Critical thinking, evidence, arguments
        - **Clarity of Thought**: Logical flow, coherence, organization
        """)
        
        if OCR_AVAILABLE and any(OCR_STATUS.values()):
            st.header("📸 Image Upload Tips")
            st.markdown("""
            - Use good lighting and avoid shadows
            - Keep the camera steady
            - Ensure text is clearly visible
            - Use high resolution images
            - Supported formats: JPG, PNG, JPEG
            """)
        
    # Main content area
    st.header("✍️ Essay Input")
    
    # Input method selection (only show if OCR is available)
    if OCR_AVAILABLE and any(OCR_STATUS.values()):
        input_method = st.radio(
            "Choose input method:",
            ["✍️ Type/Paste Text", "📸 Upload Images"],
            horizontal=True
        )
    else:
        input_method = "✍️ Type/Paste Text"
        if not OCR_AVAILABLE:
            st.info("📸 Image upload will be available after installing OCR dependencies: `pip install pillow easyocr`")
    
    essay_text = ""
    
    if input_method == "✍️ Type/Paste Text":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            essay_text = st.text_area(
                "Paste your essay here:",
                height=400,
                placeholder="Enter your UPSC essay here...",
                help="Write or paste your essay for evaluation"
            )
        
        with col2:
            st.header("🎯 Quick Tips")
            st.info("""
            **For better scores:**
            - Use clear, concise language
            - Provide specific examples
            - Structure your arguments logically
            - Stay within word limits
            - Proofread for errors
            """)
            
    elif input_method == "📸 Upload Images" and OCR_AVAILABLE:
        st.markdown("### 📸 Upload Essay Images")
        
        uploaded_files = st.file_uploader(
            "Upload images of your handwritten essay:",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="You can upload multiple images if your essay spans several pages"
        )
        
        if uploaded_files:
            st.markdown("### 🖼️ Uploaded Images Preview")
            
            # Display uploaded images in a grid
            cols = st.columns(min(3, len(uploaded_files)))
            for i, uploaded_file in enumerate(uploaded_files):
                with cols[i % 3]:
                    try:
                        image = Image.open(uploaded_file)
                        st.image(image, caption=f"Page {i+1}", use_container_width=True)
                    except Exception as e:
                        st.error(f"Error loading image {i+1}: {e}")
            
            # Process images with OCR
            if st.button("🔍 Extract Text from Images", type="secondary"):
                with st.spinner("🔄 Processing images and extracting text..."):
                    try:
                        # Check if we have any OCR engine available
                        if not any(OCR_STATUS.values()):
                            st.error("❌ No OCR engines available. Please install dependencies:")
                            st.code("pip install easyocr")
                            st.markdown("Or use the installer: `install_ocr_windows.bat`")
                            return
                        
                        # Initialize OCR processor
                        ocr_processor = SimpleOCR()
                        
                        # Show processing status
                        st.write("**Processing Status:**")
                        
                        # Process each image and show progress
                        all_text_parts = []
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i, uploaded_file in enumerate(uploaded_files):
                            status_text.text(f"Processing image {i+1} of {len(uploaded_files)}...")
                            progress_bar.progress((i) / len(uploaded_files))
                            
                            try:
                                # Load and display image info
                                image = Image.open(uploaded_file)
                                
                                # Calculate megapixels for quality assessment
                                megapixels = (image.size[0] * image.size[1]) / 1_000_000
                                
                                # Show processing info
                                with st.expander(f"📋 Image {i+1} Details", expanded=False):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write(f"**Size:** {image.size[0]} x {image.size[1]} pixels")
                                        st.write(f"**Mode:** {image.mode}")
                                        st.write(f"**Resolution:** {megapixels:.1f} MP")
                                    with col2:
                                        if megapixels < 2:
                                            st.warning("⚠️ Low resolution - may affect accuracy")
                                        elif megapixels > 20:
                                            st.info("ℹ️ High resolution - excellent for OCR")
                                        else:
                                            st.success("✅ Good resolution for OCR")
                                
                                # Extract text from this image
                                image_text = ocr_processor.extract_text(image)
                                
                                if image_text.strip():
                                    # Count words and characters
                                    word_count = len(image_text.split())
                                    char_count = len(image_text)
                                    
                                    all_text_parts.append(f"--- Page {i+1} ---\n{image_text}")
                                    st.success(f"✅ Page {i+1}: {word_count} words, {char_count} characters extracted")
                                else:
                                    all_text_parts.append(f"--- Page {i+1} ---\n[No text detected]")
                                    st.warning(f"⚠️ Page {i+1}: No text detected")
                                    
                            except Exception as e:
                                all_text_parts.append(f"--- Page {i+1} (Error) ---\nFailed to process: {str(e)}")
                                st.error(f"❌ Page {i+1}: Processing failed - {str(e)}")
                        
                        # Complete progress
                        progress_bar.progress(1.0)
                        status_text.text("Processing complete!")
                        
                        # Combine all extracted text
                        extracted_text = '\n\n'.join(all_text_parts)
                        
                        if any("No text detected" not in part and "Failed to process" not in part for part in all_text_parts):
                            st.success("✅ Text extraction completed!")
                            
                            # Show overall statistics
                            total_words = len(' '.join(all_text_parts).split())
                            total_chars = len(''.join(all_text_parts))
                            st.info(f"📊 **Total extracted:** {total_words} words, {total_chars} characters")
                            
                            # Display extracted text in an editable text area
                            st.markdown("### 📝 Extracted Text (You can edit if needed)")
                            st.info("💡 **Tip:** OCR may not be 100% accurate. Please review and correct any errors before evaluation.")
                            
                            essay_text = st.text_area(
                                "Review and edit the extracted text:",
                                value=extracted_text,
                                height=400,
                                help="Review and edit the extracted text if needed before evaluation"
                            )
                        else:
                            st.warning("⚠️ No text was extracted from the images. Please check image quality and try again.")
                            st.markdown("""
                            **Tips for better results:**
                            - Ensure good lighting and avoid shadows
                            - Use high-resolution images (at least 2MP)
                            - Make sure handwriting is clear and dark
                            - Try uploading one image at a time
                            - Ensure text is not rotated or skewed
                            - Use images with good contrast between text and background
                            """)
                    
                    except Exception as e:
                        st.error(f"❌ Error during text extraction: {str(e)}")
                        
                        # Provide specific solutions based on the error
                        if "tesseract" in str(e).lower():
                            st.markdown("""
                            **Tesseract Issue Detected:**
                            - Tesseract may not be properly installed or in PATH
                            - **Recommended solution:** Install EasyOCR instead (better for handwriting)
                            """)
                            st.code("pip install easyocr")
                            st.markdown("Then restart the app.")
                        else:
                            st.markdown("""
                            **General Solutions:**
                            - Install EasyOCR: `pip install easyocr`
                            - Check if images are valid (JPG, PNG, JPEG)
                            - Ensure images contain readable text
                            - Try with better image quality/lighting
                            - Use the installer script: `install_ocr_windows.bat`
                            """)
                            
                        # Quick install button
                        if st.button("🚀 Install EasyOCR Now", key="install_easyocr"):
                            with st.spinner("Installing EasyOCR..."):
                                st.info("Installing EasyOCR via pip. This may take a few minutes...")
                                st.warning("⚠️ Please restart the Streamlit app after installation completes.")
        else:
            st.info("📤 Please upload one or more images of your handwritten essay.")
            
        # Quick tips for image mode
        st.markdown("### 🎯 Image Upload Tips")
        st.info("""
        **For best OCR results:**
        - Use good lighting and avoid shadows
        - Keep handwriting neat and legible
        - Use dark ink on light paper
        - Capture images at high resolution
        - Ensure the entire text is visible
        - Upload pages in order for multi-page essays
        """)
    
    # Evaluation button
    if st.button("🚀 Evaluate Essay", type="primary", use_container_width=True):
        if not api_key.strip():
            st.error("❌ Please enter your OpenRouter API key in the sidebar.")
            st.info("💡 You can get your API key from https://openrouter.ai/keys")
        elif not essay_text.strip():
            st.warning("⚠️ Please enter an essay to evaluate.")
        else:
            with st.spinner("🔄 Evaluating your essay... Please wait..."):
                try:
                    # Evaluate the essay
                    result = evaluate_essay(essay_text, api_key)
                    
                    st.success("✅ Evaluation completed!")
                    st.markdown("---")
                    
                    # Display results
                    st.header("📈 Evaluation Results")
                    
                    # Overall score at the top
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.markdown(f'''
                        <div class="metric-card">
                            <h2>Overall Score</h2>
                            <h1>{result["avg_score"]:.1f}/10</h1>
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    # Individual scores
                    st.subheader("📊 Individual Scores")
                    score_col1, score_col2, score_col3 = st.columns(3)
                    
                    scores = result["individual_scores"]
                    
                    with score_col1:
                        st.markdown(f'''
                        <div class="score-box">
                            <h4>🗣️ Language Quality</h4>
                            <h2>{scores[0]}/10</h2>
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    with score_col2:
                        st.markdown(f'''
                        <div class="score-box">
                            <h4>🔍 Depth of Analysis</h4>
                            <h2>{scores[1]}/10</h2>
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    with score_col3:
                        st.markdown(f'''
                        <div class="score-box">
                            <h4>💭 Clarity of Thought</h4>
                            <h2>{scores[2]}/10</h2>
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    # Detailed feedback
                    st.subheader("📝 Detailed Feedback")
                    
                    # Language feedback
                    with st.expander("🗣️ Language Quality Feedback", expanded=True):
                        st.markdown(f'''
                        <div class="feedback-section">
                            {result["language_feedback"]}
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    # Analysis feedback
                    with st.expander("🔍 Depth of Analysis Feedback", expanded=True):
                        st.markdown(f'''
                        <div class="feedback-section">
                            {result["analysis_feedback"]}
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    # Clarity feedback
                    with st.expander("💭 Clarity of Thought Feedback", expanded=True):
                        st.markdown(f'''
                        <div class="feedback-section">
                            {result["clarity_feedback"]}
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    # Overall feedback
                    st.subheader("🎯 Overall Summary")
                    st.markdown(f'''
                    <div class="feedback-section">
                        {result["overall_feedback"]}
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Download results option
                    st.markdown("---")
                    st.subheader("💾 Download Results")
                    
                    results_text = f"""
UPSC Essay Evaluation Results
============================

Overall Score: {result["avg_score"]:.1f}/10

Individual Scores:
- Language Quality: {scores[0]}/10
- Depth of Analysis: {scores[1]}/10  
- Clarity of Thought: {scores[2]}/10

Language Quality Feedback:
{result["language_feedback"]}

Depth of Analysis Feedback:
{result["analysis_feedback"]}

Clarity of Thought Feedback:
{result["clarity_feedback"]}

Overall Summary:
{result["overall_feedback"]}
"""
                    
                    st.download_button(
                        label="📄 Download Evaluation Report",
                        data=results_text,
                        file_name="upsc_essay_evaluation.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    error_msg = str(e)
                    if "API key" in error_msg or "authentication" in error_msg.lower():
                        st.error("❌ Invalid or missing API key. Please check your OpenRouter API key.")
                        st.info("💡 Make sure you have entered a valid OpenRouter API key in the sidebar.")
                    else:
                        st.error(f"❌ An error occurred during evaluation: {error_msg}")
                        st.info("💡 Please check your API key and try again.")
                    
                    with st.expander("🔧 Troubleshooting"):
                        st.markdown("""
                        **Common issues:**
                        - Invalid API key: Check your OpenRouter API key
                        - Network connectivity issues
                        - Model availability issues
                        - Rate limiting
                        
                        **Getting help:**
                        - Visit https://openrouter.ai/keys to get your API key
                        - Check OpenRouter documentation for troubleshooting
                        """)

if __name__ == "__main__":
    main()
