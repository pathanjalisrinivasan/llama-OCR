import streamlit as st
import ollama
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Llama OCR - Extract Text Easily",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add light grey background
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description in main area
st.title("\U0001f99e OCR - Extract Text")
st.markdown("Extract text from images with precision using the powerful Llama Vision model. Ideal for structured data extraction and seamless documentation.")
st.markdown("---")

# Add clear button to top right
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("Clear \U0001f5d1\ufe0f", help="Clear all uploaded data and results"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        st.experimental_rerun()

# Move upload controls to sidebar
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'], help="Supported formats: PNG, JPG, JPEG")
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        if st.button("Extract Text \U0001f5d1\ufe0f", type="primary", help="Process the uploaded image to extract text"):
            with st.spinner("Processing image..."):
                try:
                    response = ollama.chat(
                        model='llama3.2-vision',
                        messages=[{
                            'role': 'user',
                            'content': """Analyze the text in the provided image. Extract all readable content
                                        and present it in a structured Markdown format that is clear, concise, 
                                        and well-organized. Ensure proper formatting (e.g., headings, lists, or
                                        code blocks) as necessary to represent the content effectively.""",
                            'images': [uploaded_file.getvalue()]
                        }]
                    )
                    st.session_state['ocr_result'] = response.message.content
                    st.success("Text extracted successfully! Check the results below.")
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")

# Main content area for results
if 'ocr_result' in st.session_state:
    st.markdown(st.session_state['ocr_result'])
else:
    st.info("Upload an image and click 'Extract Text' to see the results here.")
