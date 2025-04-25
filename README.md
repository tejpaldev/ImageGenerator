# Leonardo AI Clone

A Python application that replicates the functionalities of the Leonardo AI interface.

## Features

- **User Interface**:
  - Dark mode interface with a prompt input box at the top
  - Options for "Creation" and "Legacy Mode"
  - Various settings such as "Flux Ear," "Number of Images," and advanced settings
  - Option to upgrade for priority generation

- **Image Generation**:
  - Generate high-quality images based on user input
  - Support various styles and themes (e.g., realistic, abstract, cartoon)

- **Image Filtering**:
  - Apply filters to images (e.g., sepia, grayscale, blur)
  - Allow customization of filter intensity

- **Image Editing**:
  - Basic editing tools (e.g., crop, rotate, resize)
  - Advanced editing options (e.g., color correction, background removal)

- **Real-Time Preview**:
  - Display generated image sequences based on the given prompt
  - Allow users to view and select images in real-time

- **Integration**:
  - Support for importing and exporting images in various formats (e.g., JPEG, PNG, GIF)
  - Integration with cloud storage services for saving and sharing images

- **Customization**:
  - Allow users to create and save custom presets for image generation and filtering
  - Provide options for adjusting AI model parameters

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/leonardo-ai-clone.git
   cd leonardo-ai-clone
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (usually http://localhost:8501).

3. Enter a prompt in the text box and click "Generate Images" to create images based on your description.

4. Use the various tools and settings to edit, filter, and customize your generated images.

5. Export your images in your preferred format.

## Requirements

- Python 3.8 or higher
- See requirements.txt for a complete list of dependencies

## Models

The application uses the FLUX 1.1 model from Hugging Face for image generation. Other models can be integrated as needed.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project is inspired by the Leonardo AI interface
- Thanks to the creators of the FLUX models for providing open-source image generation capabilities
