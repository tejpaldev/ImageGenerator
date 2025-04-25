# Leonardo AI Clone - Simple App

A simplified version of the Leonardo AI Clone application using Tkinter for the user interface.

## Features

- **User Interface**:
  - Dark mode interface with a prompt input box
  - Options for "Creation" and "Legacy Mode"
  - Various settings such as "Flux Ear," "Number of Images," and advanced settings
  - Option to upgrade for priority generation

- **Image Generation**:
  - Generate placeholder gradient images (simulating AI generation)
  - Support for various settings like width, height, steps, and guidance scale

- **Image Filtering**:
  - Apply filters to images (Sepia, Grayscale, Blur, Sharpen)
  - Adjust filter intensity

- **Image Export**:
  - Export images in various formats (JPEG, PNG, GIF)
  - Adjust quality settings
  - Choose custom filenames

## Usage

1. Run the application:
   ```
   python simple_app.py
   ```

2. Enter a prompt in the text box and click "Generate Images" to create placeholder images.

3. Use the filter tab to apply different filters to your images.

4. Use the export tab to save your images to disk.

## Requirements

- Python 3.8 or higher
- Tkinter (included with standard Python installation)
- PIL/Pillow
- NumPy

## Notes

This is a simplified version of the Leonardo AI Clone that doesn't require external AI models or Streamlit. It uses placeholder gradient images instead of actual AI-generated images for demonstration purposes.

The full version of the application uses the FLUX 1.1 model from Hugging Face for actual AI image generation.
