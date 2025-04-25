import os
import streamlit as st
from PIL import Image
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

# Apply modern, compact theme
st.markdown("""
<style>
    /* Modern color scheme */
    :root {
        --primary-bg: #0f0f0f;
        --secondary-bg: #1a1a1a;
        --sidebar-bg: #1a1a1a;
        --card-bg: #1a1a1a;
        --primary-text: #ffffff;
        --secondary-text: #a0a0a0;
        --accent-color: #ff3366;
        --accent-hover: #ff1a53;
        --border-color: #333333;
        --input-bg: #2a2a2a;
        --button-bg: #333333;
        --button-hover: #444444;
        --success-color: #4CAF50;
        --purple-accent: #9c27b0;
    }

    /* Base styling */
    .main {
        background-color: var(--primary-bg);
        color: var(--primary-text);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }

    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--border-color);
        padding: 1rem;
    }

    /* Headers */
    h1, h2, h3 {
        color: var(--primary-text);
        font-weight: 600;
        margin-bottom: 1rem;
    }

    h1 {
        font-size: 1.8rem;
    }

    h2 {
        font-size: 1.5rem;
    }

    h3 {
        font-size: 1.2rem;
    }

    /* Form elements */
    .stTextInput, .stTextArea, .stSelectbox, .stMultiselect {
        background-color: var(--input-bg);
        color: var(--primary-text);
        border-radius: 8px;
        border: 1px solid var(--border-color);
        padding: 0.5rem;
        margin-bottom: 1rem;
    }

    /* Buttons */
    .stButton>button {
        background-color: var(--accent-color);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        background-color: var(--accent-hover);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Sliders */
    .stSlider {
        padding: 0.5rem 0;
    }

    /* Make dropdowns searchable and styled */
    .stSelectbox>div>div>div {
        background-color: var(--input-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }

    .stSelectbox>div>div>div:hover {
        border-color: var(--accent-color);
    }

    /* Cards for images */
    .image-card {
        background-color: var(--card-bg);
        border-radius: 8px;
        overflow: hidden;
        transition: transform 0.2s ease;
        border: 1px solid var(--border-color);
        margin-bottom: 1rem;
    }

    .image-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }

    /* Compact layout */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: var(--button-bg);
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1rem;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--accent-color);
        color: white;
    }

    /* Info and error messages */
    .stAlert {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 0.5rem;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        font-size: 1rem;
        font-weight: 600;
        color: var(--primary-text);
        background-color: var(--button-bg);
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }

    .streamlit-expanderContent {
        background-color: var(--card-bg);
        border-radius: 0 0 8px 8px;
        padding: 1rem;
        border: 1px solid var(--border-color);
        border-top: none;
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

# App title with modern styling
st.markdown("<h1 style='text-align: center; margin-bottom: 1.5rem;'>Leonardo AI Clone</h1>", unsafe_allow_html=True)

# Sidebar for settings with improved layout
with st.sidebar:
    st.markdown("<h3 style='margin-bottom: 1.2rem;'>⚙️ Settings</h3>", unsafe_allow_html=True)

    # Creation mode selection with modern radio buttons
    st.markdown("<p style='margin-bottom: 0.5rem; font-weight: 600;'>Mode</p>", unsafe_allow_html=True)
    creation_mode = st.radio("", ["Creation", "Legacy Mode"], label_visibility="collapsed")

    # Model selection with searchable dropdown
    st.markdown("<p style='margin-bottom: 0.5rem; margin-top: 1rem; font-weight: 600;'>Model</p>", unsafe_allow_html=True)
    model_options = ["FLUX 1.1", "FLUX Ear", "Realistic", "Abstract", "Cartoon", "Dream Shaper", "Photorealistic", "Anime Style", "Pixel Art", "3D Render"]
    model_name = st.selectbox("", model_options, label_visibility="collapsed")

    # Number of images with compact slider
    st.markdown("<p style='margin-bottom: 0.5rem; margin-top: 1rem; font-weight: 600;'>Number of Images</p>", unsafe_allow_html=True)
    num_images = st.slider("", 1, 4, 1, label_visibility="collapsed")

    # Advanced settings in a cleaner expander
    with st.expander("✨ Advanced Settings"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<p style='margin-bottom: 0.5rem; font-weight: 600;'>Width</p>", unsafe_allow_html=True)
            width = st.select_slider("", options=[512, 576, 640, 704, 768, 832, 896, 960, 1024], value=768, label_visibility="collapsed")

        with col2:
            st.markdown("<p style='margin-bottom: 0.5rem; font-weight: 600;'>Height</p>", unsafe_allow_html=True)
            height = st.select_slider("", options=[512, 576, 640, 704, 768, 832, 896, 960, 1024], value=768, label_visibility="collapsed")

        st.markdown("<p style='margin-bottom: 0.5rem; margin-top: 1rem; font-weight: 600;'>Steps</p>", unsafe_allow_html=True)
        steps = st.slider("", 1, 100, 4, label_visibility="collapsed")

        st.markdown("<p style='margin-bottom: 0.5rem; margin-top: 1rem; font-weight: 600;'>Guidance Scale</p>", unsafe_allow_html=True)
        guidance_scale = st.slider("", 1.0, 20.0, 7.5, 0.5, label_visibility="collapsed")

        st.markdown("<p style='margin-bottom: 0.5rem; margin-top: 1rem; font-weight: 600;'>Seed</p>", unsafe_allow_html=True)
        seed = st.number_input("", value=-1, label_visibility="collapsed", help="Set to -1 for random seed")

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

# Main content area with modern layout
st.markdown("""
<div style="margin-bottom: 1.5rem; background-color: var(--card-bg); padding: 1rem; border-radius: 10px; border: 1px solid var(--border-color);">
    <p style="font-size: 0.9rem; color: var(--secondary-text); margin-bottom: 0.5rem;">
        <i>💡 Tip: Be descriptive with your prompts for better results. Try including details about style, lighting, and composition.</i>
    </p>
</div>
""", unsafe_allow_html=True)

# Create a more compact layout
main_cols = st.columns([3, 4])

with main_cols[0]:
    # Prompt input with modern styling
    st.markdown("<p style='font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;'>✍️ Enter your prompt</p>", unsafe_allow_html=True)
    prompt = st.text_area("", placeholder="Describe what you want to see in detail...", height=120, label_visibility="collapsed")

    # Add some example prompts as buttons
    st.markdown("<p style='font-size: 0.8rem; margin-top: 0.5rem; margin-bottom: 0.5rem; color: var(--secondary-text);'>Try these examples:</p>", unsafe_allow_html=True)
    example_cols = st.columns(2)

    with example_cols[0]:
        if st.button("Sunset landscape", use_container_width=True):
            prompt = "A beautiful sunset over mountains with a lake in the foreground, photorealistic style"

    with example_cols[1]:
        if st.button("Sci-fi city", use_container_width=True):
            prompt = "Futuristic cyberpunk city at night with neon lights and flying cars"

    # Generate button with modern styling
    generate_btn = st.button("🚀 Generate Images", type="primary", use_container_width=True)

    # Processing logic
    if generate_btn:
        if prompt:
            with st.spinner("✨ Creating your masterpiece..."):
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

with main_cols[1]:
    # Display area for generated images with modern styling
    if st.session_state.generated_images:
        st.markdown("<p style='font-weight: 600; font-size: 1.1rem; margin-bottom: 1rem;'>🖼️ Generated Images</p>", unsafe_allow_html=True)

        # Create a grid of images with improved styling
        num_cols = min(len(st.session_state.generated_images), 2)
        image_cols = st.columns(num_cols)

        for i, img in enumerate(st.session_state.generated_images):
            with image_cols[i % num_cols]:
                # Add a container for the image with styling
                st.markdown(f"""
                <div class="image-card">
                    <p style="font-size: 0.8rem; color: var(--secondary-text); margin-bottom: 0.3rem;">Image {i+1}</p>
                </div>
                """, unsafe_allow_html=True)

                # Display the image
                st.image(img, use_column_width=True)

                # Add select button with modern styling
                if st.button(f"✅ Select", key=f"select_{i}", use_container_width=True):
                    st.session_state.current_image = img
                    st.session_state.filter_applied = None
                    st.session_state.edited_image = None
    else:
        # Empty state with better styling
        st.markdown("""
        <div style="background-color: var(--card-bg); border: 1px dashed var(--border-color); border-radius: 10px; padding: 2rem; text-align: center; margin-top: 1rem;">
            <p style="color: var(--secondary-text); font-size: 1.1rem;">✨ Your generated images will appear here</p>
            <p style="color: var(--secondary-text); font-size: 0.9rem; margin-top: 0.5rem;">Enter a prompt and click Generate to create images</p>
        </div>
        """, unsafe_allow_html=True)

# Image editing and filtering tabs with modern styling
if st.session_state.current_image is not None:
    st.markdown("<h2 style='margin-top: 2rem; margin-bottom: 1rem; font-weight: 600;'>🎨 Image Editing</h2>", unsafe_allow_html=True)

    # Create modern tabs
    tabs = st.tabs(["✨ Filters", "✏️ Edit", "💾 Export"])

    # Filters tab
    with tabs[0]:
        filter_cols = st.columns([1, 2])

        with filter_cols[0]:
            st.markdown("<p style='font-weight: 600; margin-bottom: 0.5rem;'>Select Filter</p>", unsafe_allow_html=True)
            filter_options = ["None", "Sepia", "Grayscale", "Blur", "Sharpen", "Vintage", "Noir", "Vibrant", "Pastel"]
            filter_type = st.selectbox("", filter_options, label_visibility="collapsed")

            st.markdown("<p style='font-weight: 600; margin-top: 1rem; margin-bottom: 0.5rem;'>Intensity</p>", unsafe_allow_html=True)
            intensity = st.slider("", 0.0, 1.0, 0.5, 0.1, label_visibility="collapsed")

            # Apply filter button with modern styling
            if st.button("✨ Apply Filter", use_container_width=True):
                with st.spinner("Applying artistic touch..."):
                    if filter_type != "None":
                        filtered_image = image_filter.apply_filter(
                            st.session_state.current_image,
                            filter_type,
                            intensity
                        )
                        st.session_state.filter_applied = filtered_image
                    else:
                        st.session_state.filter_applied = None

        with filter_cols[1]:
            # Image display with better styling
            st.markdown("<div style='background-color: var(--card-bg); padding: 1rem; border-radius: 10px; border: 1px solid var(--border-color);'>", unsafe_allow_html=True)

            if st.session_state.filter_applied is not None:
                st.markdown("<p style='text-align: center; font-size: 0.9rem; color: var(--secondary-text); margin-bottom: 0.5rem;'>Filtered Image</p>", unsafe_allow_html=True)
                st.image(st.session_state.filter_applied, use_column_width=True)
            else:
                st.markdown("<p style='text-align: center; font-size: 0.9rem; color: var(--secondary-text); margin-bottom: 0.5rem;'>Original Image</p>", unsafe_allow_html=True)
                st.image(st.session_state.current_image, use_column_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

    # Edit tab with modern styling
    with tabs[1]:
        edit_cols = st.columns([1, 2])

        with edit_cols[0]:
            st.markdown("<p style='font-weight: 600; margin-bottom: 0.5rem;'>Edit Operation</p>", unsafe_allow_html=True)
            edit_options = ["Crop", "Rotate", "Resize", "Color Correction", "Background Removal"]
            edit_type = st.selectbox("", edit_options, label_visibility="collapsed")

            if edit_type == "Crop":
                st.markdown("<div style='background-color: var(--input-bg); padding: 0.8rem; border-radius: 8px; margin-top: 1rem;'>", unsafe_allow_html=True)

                st.markdown("<p style='font-weight: 600; margin-bottom: 0.5rem; font-size: 0.9rem;'>Crop Margins</p>", unsafe_allow_html=True)

                crop_left = st.slider("Left", 0, 100, 0, 1, label_visibility="collapsed",
                                     help="Left margin percentage")
                st.markdown("<p style='font-size: 0.8rem; color: var(--secondary-text); margin: -0.5rem 0 0.5rem 0;'>Left: {}%</p>".format(crop_left), unsafe_allow_html=True)

                crop_top = st.slider("Top", 0, 100, 0, 1, label_visibility="collapsed",
                                    help="Top margin percentage")
                st.markdown("<p style='font-size: 0.8rem; color: var(--secondary-text); margin: -0.5rem 0 0.5rem 0;'>Top: {}%</p>".format(crop_top), unsafe_allow_html=True)

                crop_right = st.slider("Right", 0, 100, 100, 1, label_visibility="collapsed",
                                      help="Right margin percentage")
                st.markdown("<p style='font-size: 0.8rem; color: var(--secondary-text); margin: -0.5rem 0 0.5rem 0;'>Right: {}%</p>".format(crop_right), unsafe_allow_html=True)

                crop_bottom = st.slider("Bottom", 0, 100, 100, 1, label_visibility="collapsed",
                                       help="Bottom margin percentage")
                st.markdown("<p style='font-size: 0.8rem; color: var(--secondary-text); margin: -0.5rem 0 0.5rem 0;'>Bottom: {}%</p>".format(crop_bottom), unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                if st.button("✂️ Apply Crop", use_container_width=True):
                    with st.spinner("Cropping image..."):
                        edited_image = image_editor.crop(
                            st.session_state.current_image if st.session_state.filter_applied is None else st.session_state.filter_applied,
                            crop_left, crop_top, crop_right, crop_bottom
                        )
                        st.session_state.edited_image = edited_image

            elif edit_type == "Rotate":
                st.markdown("<p style='font-weight: 600; margin-top: 1rem; margin-bottom: 0.5rem;'>Rotation Angle</p>", unsafe_allow_html=True)

                angle_options = [-180, -90, -45, 0, 45, 90, 180]
                angle = st.select_slider("", options=angle_options, value=0, label_visibility="collapsed")

                st.markdown("<p style='text-align: center; font-size: 0.9rem; margin-top: 0.5rem;'>{}°</p>".format(angle), unsafe_allow_html=True)

                if st.button("🔄 Apply Rotation", use_container_width=True):
                    with st.spinner("Rotating image..."):
                        edited_image = image_editor.rotate(
                            st.session_state.current_image if st.session_state.filter_applied is None else st.session_state.filter_applied,
                            angle
                        )
                        st.session_state.edited_image = edited_image

            elif edit_type == "Resize":
                st.markdown("<div style='background-color: var(--input-bg); padding: 0.8rem; border-radius: 8px; margin-top: 1rem;'>", unsafe_allow_html=True)

                st.markdown("<p style='font-weight: 600; margin-bottom: 0.5rem; font-size: 0.9rem;'>Dimensions</p>", unsafe_allow_html=True)

                resize_width = st.number_input("Width", min_value=64, max_value=1024, value=width, step=32, label_visibility="collapsed")
                st.markdown("<p style='font-size: 0.8rem; color: var(--secondary-text); margin: -0.5rem 0 0.5rem 0;'>Width: {} px</p>".format(resize_width), unsafe_allow_html=True)

                resize_height = st.number_input("Height", min_value=64, max_value=1024, value=height, step=32, label_visibility="collapsed")
                st.markdown("<p style='font-size: 0.8rem; color: var(--secondary-text); margin: -0.5rem 0 0.5rem 0;'>Height: {} px</p>".format(resize_height), unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                if st.button("📐 Apply Resize", use_container_width=True):
                    with st.spinner("Resizing image..."):
                        edited_image = image_editor.resize(
                            st.session_state.current_image if st.session_state.filter_applied is None else st.session_state.filter_applied,
                            resize_width, resize_height
                        )
                        st.session_state.edited_image = edited_image

            elif edit_type == "Color Correction":
                st.markdown("<div style='background-color: var(--input-bg); padding: 0.8rem; border-radius: 8px; margin-top: 1rem;'>", unsafe_allow_html=True)

                st.markdown("<p style='font-weight: 600; margin-bottom: 0.5rem; font-size: 0.9rem;'>Color Adjustments</p>", unsafe_allow_html=True)

                brightness = st.slider("Brightness", 0.0, 2.0, 1.0, 0.1, label_visibility="collapsed")
                st.markdown("<p style='font-size: 0.8rem; color: var(--secondary-text); margin: -0.5rem 0 0.5rem 0;'>Brightness: {}</p>".format(brightness), unsafe_allow_html=True)

                contrast = st.slider("Contrast", 0.0, 2.0, 1.0, 0.1, label_visibility="collapsed")
                st.markdown("<p style='font-size: 0.8rem; color: var(--secondary-text); margin: -0.5rem 0 0.5rem 0;'>Contrast: {}</p>".format(contrast), unsafe_allow_html=True)

                saturation = st.slider("Saturation", 0.0, 2.0, 1.0, 0.1, label_visibility="collapsed")
                st.markdown("<p style='font-size: 0.8rem; color: var(--secondary-text); margin: -0.5rem 0 0.5rem 0;'>Saturation: {}</p>".format(saturation), unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                if st.button("🎨 Apply Color Correction", use_container_width=True):
                    with st.spinner("Adjusting colors..."):
                        edited_image = image_editor.adjust_colors(
                            st.session_state.current_image if st.session_state.filter_applied is None else st.session_state.filter_applied,
                            brightness, contrast, saturation
                        )
                        st.session_state.edited_image = edited_image

            elif edit_type == "Background Removal":
                st.markdown("<p style='margin-top: 1rem; margin-bottom: 1rem; font-size: 0.9rem; color: var(--secondary-text);'>Remove the background from your image with AI.</p>", unsafe_allow_html=True)

                if st.button("✂️ Remove Background", use_container_width=True):
                    with st.spinner("AI is working its magic..."):
                        edited_image = image_editor.remove_background(
                            st.session_state.current_image if st.session_state.filter_applied is None else st.session_state.filter_applied
                        )
                        st.session_state.edited_image = edited_image

        with edit_cols[1]:
            # Image display with better styling
            st.markdown("<div style='background-color: var(--card-bg); padding: 1rem; border-radius: 10px; border: 1px solid var(--border-color);'>", unsafe_allow_html=True)

            if st.session_state.edited_image is not None:
                st.markdown("<p style='text-align: center; font-size: 0.9rem; color: var(--secondary-text); margin-bottom: 0.5rem;'>Edited Image</p>", unsafe_allow_html=True)
                st.image(st.session_state.edited_image, use_column_width=True)
            elif st.session_state.filter_applied is not None:
                st.markdown("<p style='text-align: center; font-size: 0.9rem; color: var(--secondary-text); margin-bottom: 0.5rem;'>Filtered Image</p>", unsafe_allow_html=True)
                st.image(st.session_state.filter_applied, use_column_width=True)
            else:
                st.markdown("<p style='text-align: center; font-size: 0.9rem; color: var(--secondary-text); margin-bottom: 0.5rem;'>Original Image</p>", unsafe_allow_html=True)
                st.image(st.session_state.current_image, use_column_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

    # Export tab with modern styling
    with tabs[2]:
        export_cols = st.columns([1, 2])

        with export_cols[0]:
            st.markdown("<div style='background-color: var(--input-bg); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>", unsafe_allow_html=True)

            st.markdown("<p style='font-weight: 600; margin-bottom: 0.5rem;'>Export Format</p>", unsafe_allow_html=True)
            export_format = st.selectbox("", ["JPEG", "PNG", "GIF"], label_visibility="collapsed")

            st.markdown("<p style='font-weight: 600; margin-top: 1rem; margin-bottom: 0.5rem;'>Quality</p>", unsafe_allow_html=True)
            export_quality = st.slider("", 1, 100, 95, 1, label_visibility="collapsed")
            st.markdown("<p style='font-size: 0.8rem; color: var(--secondary-text); text-align: center; margin-top: -0.5rem;'>{}/100</p>".format(export_quality), unsafe_allow_html=True)

            st.markdown("<p style='font-weight: 600; margin-top: 1rem; margin-bottom: 0.5rem;'>Filename</p>", unsafe_allow_html=True)
            export_filename = st.text_input("", value="leonardo_ai_image", label_visibility="collapsed", placeholder="Enter filename without extension")

            st.markdown("</div>", unsafe_allow_html=True)

            # Export button with modern styling
            if st.button("💾 Export Image", use_container_width=True, type="primary"):
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
                    st.success(f"✅ Image exported successfully to {export_path}")
                else:
                    st.error("❌ Failed to export image")

            # Add format info
            st.markdown("""
            <div style="margin-top: 1rem; padding: 0.8rem; background-color: var(--card-bg); border-radius: 8px; font-size: 0.9rem; color: var(--secondary-text);">
                <p style="margin-bottom: 0.5rem;"><strong>Format Info:</strong></p>
                <ul style="margin-left: 1rem; margin-bottom: 0;">
                    <li>PNG: Best for transparency, larger file size</li>
                    <li>JPEG: Smaller file size, no transparency</li>
                    <li>GIF: Good for simple images, limited colors</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with export_cols[1]:
            # Image display with better styling
            st.markdown("<div style='background-color: var(--card-bg); padding: 1rem; border-radius: 10px; border: 1px solid var(--border-color);'>", unsafe_allow_html=True)

            image_to_display = (st.session_state.edited_image if st.session_state.edited_image is not None
                              else st.session_state.filter_applied if st.session_state.filter_applied is not None
                              else st.session_state.current_image)

            st.markdown("<p style='text-align: center; font-size: 0.9rem; color: var(--secondary-text); margin-bottom: 0.5rem;'>Image Preview</p>", unsafe_allow_html=True)
            st.image(image_to_display, use_column_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

            # Download button with modern styling
            if image_to_display is not None:
                # Convert image to bytes for download
                img_bytes = file_handler.image_to_bytes(
                    image_to_display,
                    format=export_format.lower(),
                    quality=export_quality
                )

                st.markdown("<p style='text-align: center; margin-top: 1rem;'>", unsafe_allow_html=True)
                st.download_button(
                    label="⬇️ Download Image",
                    data=img_bytes,
                    file_name=f"{export_filename}.{export_format.lower()}",
                    mime=f"image/{export_format.lower()}",
                    use_container_width=True
                )
                st.markdown("</p>", unsafe_allow_html=True)

                # Add image details
                st.markdown(f"""
                <div style="margin-top: 1rem; padding: 0.8rem; background-color: var(--input-bg); border-radius: 8px; font-size: 0.9rem;">
                    <p style="margin-bottom: 0.3rem;"><strong>File Details:</strong></p>
                    <p style="margin-bottom: 0.2rem; color: var(--secondary-text);">Format: {export_format}</p>
                    <p style="margin-bottom: 0.2rem; color: var(--secondary-text);">Quality: {export_quality}%</p>
                    <p style="margin-bottom: 0; color: var(--secondary-text);">Filename: {export_filename}.{export_format.lower()}</p>
                </div>
                """, unsafe_allow_html=True)

# Modern footer
st.markdown("""
<footer style="margin-top: 3rem; padding: 1.5rem; background-color: var(--card-bg); border-radius: 10px; text-align: center; border-top: 1px solid var(--border-color);">
    <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 1rem;">
        <div>
            <p style="font-weight: 600; margin-bottom: 0.5rem;">Leonardo AI Clone</p>
            <p style="font-size: 0.9rem; color: var(--secondary-text);">Create stunning AI-generated images</p>
        </div>
        <div>
            <p style="font-weight: 600; margin-bottom: 0.5rem;">Resources</p>
            <p style="font-size: 0.9rem; color: var(--secondary-text);">Documentation | Support | API</p>
        </div>
        <div>
            <p style="font-weight: 600; margin-bottom: 0.5rem;">Connect</p>
            <p style="font-size: 0.9rem; color: var(--secondary-text);">Twitter | Discord | GitHub</p>
        </div>
    </div>
    <p style="font-size: 0.8rem; color: var(--secondary-text); margin-bottom: 0;">© 2025 Leonardo AI Clone. All rights reserved.</p>
</footer>
""", unsafe_allow_html=True)
