import os
import streamlit as st
from PIL import Image
import torch
import numpy as np
import time
from models.image_generator import ImageGenerator
from models.image_filter import ImageFilter
from models.image_editor import ImageEditor
from utils.file_handler import FileHandler

# Set page configuration
st.set_page_config(
    page_title="Leonardo AI Clone",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Leonardo AI Clone\nA Python application that replicates the functionalities of the Leonardo AI interface."
    }
)

# Apply dark theme
st.markdown("""
<style>
    .main {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stTextInput, .stSelectbox, .stSlider {
        background-color: #2D2D2D;
        color: #FFFFFF;
        border-radius: 5px;
    }
    .stButton>button {
        background-color: #4F4F4F;
        color: #FFFFFF;
    }
    .stButton>button:hover {
        background-color: #6E6E6E;
        color: #FFFFFF;
    }
    .sidebar .sidebar-content {
        background-color: #2D2D2D;
    }
    h1, h2, h3 {
        color: #FFFFFF;
    }
    .upgrade-banner {
        background-color: #3D3D3D;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        border: 1px solid #5D5D5D;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []
if 'current_image' not in st.session_state:
    st.session_state.current_image = None
if 'filter_applied' not in st.session_state:
    st.session_state.filter_applied = None
if 'edited_image' not in st.session_state:
    st.session_state.edited_image = None

# Initialize components
image_generator = ImageGenerator()
image_filter = ImageFilter()
image_editor = ImageEditor()
file_handler = FileHandler()

# App title
st.title("Leonardo AI Clone")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    
    # Creation mode selection
    creation_mode = st.radio("Mode", ["Creation", "Legacy Mode"])
    
    # Model selection
    model_name = st.selectbox("Model", ["FLUX 1.1", "FLUX Ear", "Realistic", "Abstract", "Cartoon"])
    
    # Number of images
    num_images = st.slider("Number of Images", 1, 4, 1)
    
    # Advanced settings
    with st.expander("Advanced Settings"):
        width = st.slider("Width", 512, 1024, 768, 64)
        height = st.slider("Height", 512, 1024, 768, 64)
        steps = st.slider("Steps", 20, 100, 50)
        guidance_scale = st.slider("Guidance Scale", 1.0, 20.0, 7.5, 0.5)
        seed = st.number_input("Seed", value=-1, help="Set to -1 for random seed")
    
    # Upgrade banner
    st.markdown("""
    <div class="upgrade-banner">
        <h3>Upgrade for Priority Generation</h3>
        <p>Get faster generation times and priority in the queue.</p>
        <button style="background-color: #4CAF50; color: white; padding: 10px; border: none; border-radius: 5px; cursor: pointer; width: 100%;">
            Upgrade Now
        </button>
    </div>
    """, unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([2, 3])

with col1:
    # Prompt input
    st.subheader("Enter your prompt")
    prompt = st.text_area("Be descriptive for better results", height=100)
    
    # Generate button
    if st.button("Generate Images", type="primary"):
        if prompt:
            with st.spinner("Generating images..."):
                # Generate images
                images = image_generator.generate(
                    prompt=prompt,
                    num_images=num_images,
                    width=width,
                    height=height,
                    steps=steps,
                    guidance_scale=guidance_scale,
                    seed=seed if seed != -1 else None
                )
                
                st.session_state.generated_images = images
                if images:
                    st.session_state.current_image = images[0]
                    st.session_state.filter_applied = None
                    st.session_state.edited_image = None
        else:
            st.error("Please enter a prompt first.")

with col2:
    # Display area for generated images
    if st.session_state.generated_images:
        st.subheader("Generated Images")
        
        # Create a grid of images
        image_cols = st.columns(min(len(st.session_state.generated_images), 2))
        for i, img in enumerate(st.session_state.generated_images):
            with image_cols[i % 2]:
                st.image(img, use_column_width=True)
                if st.button(f"Select Image {i+1}", key=f"select_{i}"):
                    st.session_state.current_image = img
                    st.session_state.filter_applied = None
                    st.session_state.edited_image = None
    else:
        st.info("Generated images will appear here.")

# Image editing and filtering tabs
if st.session_state.current_image is not None:
    st.header("Image Editing")
    tabs = st.tabs(["Filters", "Edit", "Export"])
    
    # Filters tab
    with tabs[0]:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            filter_type = st.selectbox("Select Filter", ["None", "Sepia", "Grayscale", "Blur", "Sharpen", "Vintage"])
            intensity = st.slider("Intensity", 0.0, 1.0, 0.5, 0.1)
            
            if st.button("Apply Filter"):
                with st.spinner("Applying filter..."):
                    if filter_type != "None":
                        filtered_image = image_filter.apply_filter(
                            st.session_state.current_image, 
                            filter_type, 
                            intensity
                        )
                        st.session_state.filter_applied = filtered_image
                    else:
                        st.session_state.filter_applied = None
        
        with col2:
            if st.session_state.filter_applied is not None:
                st.image(st.session_state.filter_applied, caption="Filtered Image", use_column_width=True)
            else:
                st.image(st.session_state.current_image, caption="Original Image", use_column_width=True)
    
    # Edit tab
    with tabs[1]:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            edit_type = st.selectbox("Edit Operation", ["Crop", "Rotate", "Resize", "Color Correction", "Background Removal"])
            
            if edit_type == "Crop":
                crop_left = st.slider("Left", 0, 100, 0, 1)
                crop_top = st.slider("Top", 0, 100, 0, 1)
                crop_right = st.slider("Right", 0, 100, 100, 1)
                crop_bottom = st.slider("Bottom", 0, 100, 100, 1)
                
                if st.button("Apply Crop"):
                    with st.spinner("Cropping image..."):
                        edited_image = image_editor.crop(
                            st.session_state.current_image if st.session_state.filter_applied is None else st.session_state.filter_applied,
                            crop_left, crop_top, crop_right, crop_bottom
                        )
                        st.session_state.edited_image = edited_image
            
            elif edit_type == "Rotate":
                angle = st.slider("Angle", -180, 180, 0, 5)
                
                if st.button("Apply Rotation"):
                    with st.spinner("Rotating image..."):
                        edited_image = image_editor.rotate(
                            st.session_state.current_image if st.session_state.filter_applied is None else st.session_state.filter_applied,
                            angle
                        )
                        st.session_state.edited_image = edited_image
            
            elif edit_type == "Resize":
                resize_width = st.slider("Width", 64, 1024, width, 32)
                resize_height = st.slider("Height", 64, 1024, height, 32)
                
                if st.button("Apply Resize"):
                    with st.spinner("Resizing image..."):
                        edited_image = image_editor.resize(
                            st.session_state.current_image if st.session_state.filter_applied is None else st.session_state.filter_applied,
                            resize_width, resize_height
                        )
                        st.session_state.edited_image = edited_image
            
            elif edit_type == "Color Correction":
                brightness = st.slider("Brightness", 0.0, 2.0, 1.0, 0.1)
                contrast = st.slider("Contrast", 0.0, 2.0, 1.0, 0.1)
                saturation = st.slider("Saturation", 0.0, 2.0, 1.0, 0.1)
                
                if st.button("Apply Color Correction"):
                    with st.spinner("Adjusting colors..."):
                        edited_image = image_editor.adjust_colors(
                            st.session_state.current_image if st.session_state.filter_applied is None else st.session_state.filter_applied,
                            brightness, contrast, saturation
                        )
                        st.session_state.edited_image = edited_image
            
            elif edit_type == "Background Removal":
                if st.button("Remove Background"):
                    with st.spinner("Removing background..."):
                        edited_image = image_editor.remove_background(
                            st.session_state.current_image if st.session_state.filter_applied is None else st.session_state.filter_applied
                        )
                        st.session_state.edited_image = edited_image
        
        with col2:
            if st.session_state.edited_image is not None:
                st.image(st.session_state.edited_image, caption="Edited Image", use_column_width=True)
            elif st.session_state.filter_applied is not None:
                st.image(st.session_state.filter_applied, caption="Filtered Image", use_column_width=True)
            else:
                st.image(st.session_state.current_image, caption="Original Image", use_column_width=True)
    
    # Export tab
    with tabs[2]:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            export_format = st.selectbox("Export Format", ["JPEG", "PNG", "GIF"])
            export_quality = st.slider("Quality", 1, 100, 95, 1)
            export_filename = st.text_input("Filename", "leonardo_ai_image")
            
            if st.button("Export Image"):
                image_to_export = (st.session_state.edited_image if st.session_state.edited_image is not None 
                                  else st.session_state.filter_applied if st.session_state.filter_applied is not None 
                                  else st.session_state.current_image)
                
                export_path = file_handler.save_image(
                    image_to_export,
                    export_filename,
                    export_format.lower(),
                    export_quality
                )
                
                if export_path:
                    st.success(f"Image exported successfully to {export_path}")
                else:
                    st.error("Failed to export image")
        
        with col2:
            image_to_display = (st.session_state.edited_image if st.session_state.edited_image is not None 
                              else st.session_state.filter_applied if st.session_state.filter_applied is not None 
                              else st.session_state.current_image)
            
            st.image(image_to_display, caption="Image to Export", use_column_width=True)
            
            # Download button
            if image_to_display is not None:
                # Convert image to bytes for download
                img_bytes = file_handler.image_to_bytes(
                    image_to_display, 
                    format=export_format.lower(), 
                    quality=export_quality
                )
                
                st.download_button(
                    label="Download Image",
                    data=img_bytes,
                    file_name=f"{export_filename}.{export_format.lower()}",
                    mime=f"image/{export_format.lower()}"
                )

# Footer
st.markdown("---")
st.markdown("© 2025 Leonardo AI Clone. All rights reserved.")
