# Leonardo AI Clone - Web Application

A web-based version of the Leonardo AI Clone application using Flask for the backend and modern web technologies for the frontend.

## Features

- **User Interface**:
  - Dark mode interface with a prompt input box
  - Options for "Creation" and "Legacy Mode"
  - Various settings such as model selection, number of images, and advanced parameters
  - Option to upgrade for priority generation

- **Image Generation**:
  - Generate placeholder gradient images (simulating AI generation)
  - Support for various settings like width, height, steps, and guidance scale

- **Image Filtering**:
  - Apply filters to images (Sepia, Grayscale, Blur, Sharpen)
  - Adjust filter intensity with a slider

- **Image Export**:
  - Export images in various formats (JPEG, PNG, GIF)
  - Adjust quality settings
  - Choose custom filenames

## Installation

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the web application:
   ```
   python web_app.py
   ```

3. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Project Structure

- `web_app.py` - Main Flask application
- `templates/index.html` - HTML template for the web interface
- `static/css/style.css` - CSS styling for the application
- `static/js/main.js` - JavaScript for frontend interactivity
- `static/uploads/` - Directory for storing generated images

## Future Enhancements

1. **Integrate Real AI Models**:
   - Replace the placeholder image generation with actual FLUX 1.1 model integration
   - This would require installing the necessary dependencies and ensuring they're in your PATH

2. **Add More Editing Features**:
   - Implement the editing tab functionality for crop, rotate, resize, etc.
   - Add more advanced filters and effects

3. **Improve the UI**:
   - Add more visual feedback during image generation
   - Implement drag-and-drop functionality for importing images

## Notes

This is a web-based version of the Leonardo AI Clone that uses Flask for the backend. It currently uses placeholder gradient images instead of actual AI-generated images for demonstration purposes.

The full version of the application would use the FLUX 1.1 model from Hugging Face for actual AI image generation.
