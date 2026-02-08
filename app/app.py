import streamlit as st
import time
import os
from PIL import Image
from datetime import datetime

# Import NeuroMorph system
from prompts import PROMPTS, SETTINGS
from engine import NeuroMorph
from config import OUTPUT_DIR

# Import Cloudinary utils
from cloud_manager import upload_and_generate_qr

st.set_page_config(page_title="NeuroMorph", layout="centered")

# Custom CSS for icons
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .icon-text {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .stButton button {
            width: 100%;
        }
        .result-container {
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            background-color: #f0f8f0;
        }
        .error-container {
            border: 2px solid #f44336;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            background-color: #fff0f0;
        }
        .qr-container {
            border: 2px solid #2196F3;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            background-color: #e3f2fd;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize NeuroMorph (cached to avoid reloading)
@st.cache_resource
def load_neuromorph():
    """Load and setup NeuroMorph model (cached)"""
    status_placeholder = st.empty()
    status_placeholder.markdown('<p><i class="fas fa-cog fa-spin"></i> Loading AI models... This may take a minute on first run.</p>', unsafe_allow_html=True)
    
    try:
        morph = NeuroMorph()
        morph.setup()
        status_placeholder.empty()
        return morph
    except Exception as e:
        status_placeholder.error(f"Failed to load models: {str(e)}")
        return None

# Save uploaded image temporarily
def save_temp_image(uploaded_file):
    """Save uploaded image to temporary file"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    temp_path = os.path.join(OUTPUT_DIR, f"temp_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    
    image = Image.open(uploaded_file)
    image.save(temp_path)
    return temp_path

st.markdown('<h1 style="text-align: center;"><i class="fas fa-palette"></i> NeuroMorph</h1>', unsafe_allow_html=True)
st.markdown("---")

# Initialize session state
if 'captured_image' not in st.session_state:
    st.session_state.captured_image = None
if 'generated_image' not in st.session_state:
    st.session_state.generated_image = None
if 'temp_image_path' not in st.session_state:
    st.session_state.temp_image_path = None
if 'generation_time' not in st.session_state:
    st.session_state.generation_time = None
if 'public_url' not in st.session_state:
    st.session_state.public_url = None
if 'qr_code' not in st.session_state:
    st.session_state.qr_code = None

st.markdown("<br>", unsafe_allow_html=True)

# Camera Input
st.markdown('<h3><i class="fas fa-camera"></i> Input 1: Camera</h3>', unsafe_allow_html=True)
camera_photo = st.camera_input("Take a photo", label_visibility="collapsed")

if camera_photo is not None:
    st.session_state.captured_image = camera_photo
    st.markdown('<div class="result-container"><i class="fas fa-check-circle"></i> Photo captured successfully!</div>', unsafe_allow_html=True)

# Display captured image
if st.session_state.captured_image is not None:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.image(st.session_state.captured_image, caption="Captured Image", use_container_width=True)
    with col2:
        if st.button("Retake", key="retake_btn"):
            st.session_state.captured_image = None
            st.session_state.generated_image = None
            st.session_state.temp_image_path = None
            st.session_state.generation_time = None
            st.session_state.public_url = None
            st.session_state.qr_code = None
            st.rerun()

st.markdown("---")

# Style selector
st.markdown('<h3><i class="fas fa-brush"></i> Select Style</h3>', unsafe_allow_html=True)
style_options = ["anime", "ghibli", "zootopia"]
selected_style = st.selectbox(
    "Choose style:",
    options=style_options,
    index=0,
    label_visibility="collapsed"
)

# Advanced settings (optional)
with st.expander("Advanced Settings"):
    col1, col2 = st.columns(2)
    
    with col1:
        steps = st.slider("Inference Steps", min_value=20, max_value=50, value=SETTINGS[selected_style]["steps"], step=5)
        strength = st.slider("Transformation Strength", min_value=0.3, max_value=0.8, value=SETTINGS[selected_style]["strength"], step=0.05)
    
    with col2:
        lora_scale = st.slider("LoRA Scale", min_value=0.5, max_value=1.0, value=SETTINGS[selected_style]["lora_scale"], step=0.05)
        guidance_scale = st.slider("Guidance Scale", min_value=5.0, max_value=12.0, value=SETTINGS[selected_style]["guidance_scale"], step=0.5)

st.markdown("---")

# Submit button
st.markdown('<div style="display: flex; justify-content: end;">', unsafe_allow_html=True)
submit_button = st.button("Generate Style Transfer", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Processing with interactive loading
if submit_button:
    if st.session_state.captured_image is None:
        st.markdown('<div class="error-container"><i class="fas fa-exclamation-triangle"></i> Please capture a photo first!</div>', unsafe_allow_html=True)
    else:
        try:
            # Load model
            neuromorph = load_neuromorph()
            
            if neuromorph is None:
                st.markdown('<div class="error-container"><i class="fas fa-times-circle"></i> Failed to load AI models. Please check your configuration.</div>', unsafe_allow_html=True)
            else:
                # Save temporary image
                st.session_state.temp_image_path = save_temp_image(st.session_state.captured_image)
                
                # Get prompts for selected style
                positive_prompt = PROMPTS[selected_style]["positive"]
                negative_prompt = PROMPTS[selected_style]["negative"]
                
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Step 1: Preprocessing
                status_text.markdown('<p><i class="fas fa-spinner fa-spin"></i> Preprocessing image...</p>', unsafe_allow_html=True)
                progress_bar.progress(15)
                time.sleep(0.3)
                
                # Step 2: AI Generation
                status_text.markdown(f'<p><i class="fas fa-spinner fa-spin"></i> Applying {selected_style} style with AI...</p>', unsafe_allow_html=True)
                progress_bar.progress(30)
                
                # Actual generation
                start_time = time.time()
                result_image = neuromorph.generate(
                    image_path=st.session_state.temp_image_path,
                    prompt=positive_prompt,
                    negative_prompt=negative_prompt,
                    steps=steps,
                    strength=strength,
                    lora_scale=lora_scale
                )
                generation_time = time.time() - start_time
                st.session_state.generation_time = generation_time
                
                progress_bar.progress(60)
                
                # Step 3: Face enhancement
                status_text.markdown('<p><i class="fas fa-spinner fa-spin"></i> Enhancing facial details...</p>', unsafe_allow_html=True)
                progress_bar.progress(70)
                time.sleep(0.3)
                
                # Step 4: Uploading to Cloudinary
                status_text.markdown('<p><i class="fas fa-spinner fa-spin"></i> Uploading to cloud storage...</p>', unsafe_allow_html=True)
                progress_bar.progress(80)
                
                try:
                    public_url, qr_code = upload_and_generate_qr(result_image, selected_style)
                    st.session_state.public_url = public_url
                    st.session_state.qr_code = qr_code
                except Exception as e:
                    st.warning(f"Cloud upload failed: {str(e)}. Image saved locally only.")
                
                progress_bar.progress(90)
                
                # Step 5: Finalizing
                status_text.markdown('<p><i class="fas fa-spinner fa-spin"></i> Finalizing output...</p>', unsafe_allow_html=True)
                progress_bar.progress(100)
                
                # Save result locally
                output_filename = f"result_{selected_style}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                output_path = os.path.join(OUTPUT_DIR, output_filename)
                result_image.save(output_path)
                
                st.session_state.generated_image = result_image
                
                status_text.markdown('<p><i class="fas fa-check-circle"></i> Processing complete!</p>', unsafe_allow_html=True)
                time.sleep(0.5)
                
                progress_bar.empty()
                status_text.empty()
                
                st.markdown('<div class="result-container"><i class="fas fa-check-circle"></i> Style transfer completed successfully!</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.markdown(f'<div class="error-container"><i class="fas fa-times-circle"></i> Error during generation: {str(e)}</div>', unsafe_allow_html=True)

# Display results
if st.session_state.generated_image is not None:
    st.markdown("---")
    st.markdown('<h3><i class="fas fa-image"></i> Results</h3>', unsafe_allow_html=True)
    
    with st.expander("Result Details", expanded=True):
        st.write(f"**Selected Style:** {selected_style.capitalize()}")
        
        if st.session_state.generation_time:
            st.write(f"**Generation Time:** {st.session_state.generation_time:.2f} seconds")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Original Image**")
            st.image(st.session_state.captured_image, use_container_width=True)
        
        with col2:
            st.markdown(f"**{selected_style.capitalize()} Style**")
            st.image(st.session_state.generated_image, use_container_width=True)
        
        # Download button
        from io import BytesIO
        buf = BytesIO()
        st.session_state.generated_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="Download Result",
            data=byte_im,
            file_name=f"ai_style_{selected_style}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            mime="image/png",
            icon=":material/download:"
        )
    
    # QR Code Section
    if st.session_state.qr_code is not None and st.session_state.public_url is not None:
        st.markdown("---")
        st.markdown('<h3><i class="fas fa-qrcode"></i> QR Code & Share</h3>', unsafe_allow_html=True)
        
        with st.expander("QR Code for Download", expanded=True):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.image(st.session_state.qr_code, caption="Scan to Download", use_container_width=True)
            
            with col2:
                st.markdown('<div class="qr-container">', unsafe_allow_html=True)
                st.markdown('<p><i class="fas fa-info-circle"></i> <strong>How to use:</strong></p>', unsafe_allow_html=True)
                st.markdown("""
                1. Scan QR code with your smartphone
                2. Download image directly to your device
                3. Share with friends!
                """)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown(f"**Public URL:** [{st.session_state.public_url}]({st.session_state.public_url})")
                
                # Copy URL button
                st.code(st.session_state.public_url, language=None)

st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: gray;"><i class="fas fa-info-circle"></i> Tip: Capture a clear photo and select your style before submitting</div>',
    unsafe_allow_html=True
)