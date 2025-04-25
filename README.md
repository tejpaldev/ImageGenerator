# Leonardo AI Clone

A web-based AI image generation application that uses the Together API with the FLUX.1-schnell model.

## Features

- **Modern User Interface**:
  - Elegant, compact dark mode interface with searchable dropdowns
  - Options for "Creation" and "Legacy Mode"
  - Various settings such as model selection, image dimensions, and advanced parameters
  - Intuitive image editing and filtering tools

- **Image Generation**:
  - Generate high-quality images using Together API with FLUX.1-schnell model
  - Support for various styles and themes (realistic, abstract, cartoon, etc.)
  - Customizable parameters like steps, guidance scale, and seed

- **Image Filtering**:
  - Apply filters to images (sepia, grayscale, blur, sharpen, vintage, etc.)
  - Adjustable filter intensity

- **Image Editing**:
  - Basic editing tools (crop, rotate, resize)
  - Advanced editing options (color correction, background removal)

- **Real-Time Preview**:
  - Display generated image sequences based on the given prompt
  - Interactive image selection and editing

- **Export Options**:
  - Support for exporting images in various formats (JPEG, PNG, GIF)
  - Adjustable quality settings for exports

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/leonardo-ai-clone.git
   cd leonardo-ai-clone
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your Together API key:
   ```
   TOGETHER_API_KEY=your_api_key_here
   ```

## Usage

### Streamlit App (Recommended)

1. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (usually http://localhost:8501).

3. Enter a prompt in the text box and click "Generate Images" to create images based on your description.

4. Use the various tools and settings to edit, filter, and customize your generated images.

5. Export your images in your preferred format.

### Flask Web App

1. Run the Flask web application:
   ```
   python web_app.py
   ```

2. Open your web browser and navigate to http://localhost:5000 (or the port shown in the terminal).

## Requirements

- Python 3.8 or higher
- flask>=2.0.0
- pillow>=9.0.0
- numpy>=1.24.0
- streamlit>=1.22.0
- together>=0.1.5
- python-dotenv>=1.0.0
- opencv-python>=4.7.0 (for background removal)

## Models

The application uses the FLUX.1-schnell model from Black Forest Labs via the Together API for image generation.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project is inspired by the Leonardo AI interface
- Thanks to the creators of the FLUX models for providing open-source image generation capabilities
