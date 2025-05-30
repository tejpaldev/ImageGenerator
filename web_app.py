import os
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import io
from flask import Flask, render_template, request, jsonify, send_file, url_for
import uuid
from models.image_generator import ImageGenerator

class ImageFilter:
    def __init__(self):
        """
        Initialize the ImageFilter class.
        """
        pass

    def apply_filter(self, image, filter_type, intensity=0.5):
        """
        Apply a filter to the image.

        Args:
            image (PIL.Image): Input image
            filter_type (str): Type of filter to apply
            intensity (float): Intensity of the filter (0.0 to 1.0)

        Returns:
            PIL.Image: Filtered image
        """
        try:
            if filter_type == "Sepia":
                return self.sepia_filter(image, intensity)
            elif filter_type == "Grayscale":
                return self.grayscale_filter(image, intensity)
            elif filter_type == "Blur":
                return self.blur_filter(image, intensity)
            elif filter_type == "Sharpen":
                return self.sharpen_filter(image, intensity)
            else:
                return image
        except Exception as e:
            print(f"Error applying filter: {e}")
            return image

    def sepia_filter(self, image, intensity=0.5):
        """
        Apply a sepia filter to the image.

        Args:
            image (PIL.Image): Input image
            intensity (float): Intensity of the filter (0.0 to 1.0)

        Returns:
            PIL.Image: Filtered image
        """
        # Convert to grayscale
        grayscale = ImageOps.grayscale(image)

        # Apply sepia tone
        sepia = ImageOps.colorize(grayscale, "#000", "#EBC")

        # Blend with original based on intensity
        return Image.blend(image, sepia, intensity)

    def grayscale_filter(self, image, intensity=0.5):
        """
        Apply a grayscale filter to the image.

        Args:
            image (PIL.Image): Input image
            intensity (float): Intensity of the filter (0.0 to 1.0)

        Returns:
            PIL.Image: Filtered image
        """
        # Convert to grayscale
        grayscale_image = ImageOps.grayscale(image)
        grayscale_image = grayscale_image.convert('RGB')

        # Blend with original based on intensity
        return Image.blend(image, grayscale_image, intensity)

    def blur_filter(self, image, intensity=0.5):
        """
        Apply a blur filter to the image.

        Args:
            image (PIL.Image): Input image
            intensity (float): Intensity of the filter (0.0 to 1.0)

        Returns:
            PIL.Image: Filtered image
        """
        # Calculate blur radius based on intensity
        radius = int(10 * intensity)
        if radius < 1:
            radius = 1

        # Apply Gaussian blur
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=radius))

        return blurred_image

    def sharpen_filter(self, image, intensity=0.5):
        """
        Apply a sharpen filter to the image.

        Args:
            image (PIL.Image): Input image
            intensity (float): Intensity of the filter (0.0 to 1.0)

        Returns:
            PIL.Image: Filtered image
        """
        # Create a sharpened version
        enhancer = ImageEnhance.Sharpness(image)
        sharpened_image = enhancer.enhance(1.0 + 4.0 * intensity)

        return sharpened_image

class LeonardoAI:
    def __init__(self):
        """
        Initialize the LeonardoAI class.
        """
        self.image_generator = ImageGenerator()
        self.image_filter = ImageFilter()
        self.generated_images = {}
        self.user_tokens = 150  # Default token balance

    def generate_images(self, prompt, num_images=1, width=1024, height=768, steps=4, guidance_scale=7.5, seed=None, model="FLUX 1.1"):
        """
        Generate images and manage token usage.

        Args:
            prompt (str): Text prompt for image generation
            num_images (int): Number of images to generate
            width (int): Width of the generated images
            height (int): Height of the generated images
            steps (int): Number of denoising steps
            guidance_scale (float): Guidance scale for the model
            seed (int, optional): Random seed for reproducibility
            model (str): Model name to use for generation

        Returns:
            dict: Generation results including session ID and image URLs
        """
        # Calculate token cost (simplified for demo)
        token_cost = num_images * 0.4

        # Check if user has enough tokens
        if self.user_tokens < token_cost:
            return {
                'success': False,
                'error': 'Not enough tokens. Please upgrade your plan.'
            }

        # Generate images - model parameter is not used by the API but stored for reference
        images = self.image_generator.generate(
            prompt=prompt,
            num_images=num_images,
            width=width,
            height=height,
            steps=steps,
            guidance_scale=guidance_scale,
            seed=seed
        )

        # Create a unique session ID for this generation
        session_id = str(uuid.uuid4())

        # Save images to memory and disk
        image_urls = []
        for i, img in enumerate(images):
            # Save to disk
            filename = f"{session_id}_{i}.png"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img.save(filepath)

            # Add to memory storage
            if session_id not in self.generated_images:
                self.generated_images[session_id] = []
            self.generated_images[session_id].append({
                'id': i,
                'path': filepath,
                'url': url_for('static', filename=f'uploads/{filename}'),
                'prompt': prompt,
                'model': model,
                'width': width,
                'height': height
            })

            # Add URL to response
            image_urls.append(url_for('static', filename=f'uploads/{filename}'))

        # Deduct tokens
        self.user_tokens -= token_cost

        return {
            'success': True,
            'session_id': session_id,
            'images': image_urls,
            'remaining_tokens': self.user_tokens
        }

    def apply_filter(self, session_id, image_id, filter_type, intensity=0.5):
        """
        Apply a filter to a generated image.

        Args:
            session_id (str): Session ID
            image_id (int): Image ID
            filter_type (str): Type of filter to apply
            intensity (float): Intensity of the filter (0.0 to 1.0)

        Returns:
            dict: Filter results
        """
        # Check if session and image exist
        if session_id not in self.generated_images or image_id >= len(self.generated_images[session_id]):
            return {
                'success': False,
                'error': 'Image not found'
            }

        # Get the image
        image_path = self.generated_images[session_id][image_id]['path']
        image = Image.open(image_path)

        # Apply filter
        if filter_type != 'None':
            filtered_image = self.image_filter.apply_filter(image, filter_type, intensity)
        else:
            filtered_image = image

        # Save filtered image
        filtered_filename = f"{session_id}_{image_id}_filtered.png"
        filtered_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filtered_filename)
        filtered_image.save(filtered_filepath)

        # Update memory storage
        self.generated_images[session_id][image_id]['filtered_path'] = filtered_filepath
        self.generated_images[session_id][image_id]['filtered_url'] = url_for('static', filename=f'uploads/{filtered_filename}')

        return {
            'success': True,
            'filtered_image': url_for('static', filename=f'uploads/{filtered_filename}')
        }

    def get_token_balance(self):
        """
        Get the current token balance.

        Returns:
            int: Current token balance
        """
        return self.user_tokens

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Leonardo AI
leonardo_ai = LeonardoAI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_images():
    # Get parameters from form
    prompt = request.form.get('prompt', '')
    num_images = int(request.form.get('num_images', 1))
    width = int(request.form.get('width', 1024))
    height = int(request.form.get('height', 768))
    steps = int(request.form.get('steps', 4))
    guidance_scale = float(request.form.get('guidance_scale', 7.5))
    seed = request.form.get('seed', '-1')

    # Handle model selection with fallbacks
    model = request.form.get('model', '')
    if not model:
        model = request.form.get('preset', '')  # Try 'preset' if 'model' is empty
    if not model:
        model = 'FLUX 1.1'  # Default if neither is provided

    # Handle additional UI parameters (these don't affect API calls but are logged)
    format_enhance = request.form.get('format_enhance', 'Auto')
    style = request.form.get('style', 'Dynamic')

    # Map UI model names to API model names if needed
    model_mapping = {
        'Flux Dev': 'FLUX 1.1',
        'Flux': 'FLUX 1.1',
        # Add more mappings as needed
    }

    # Use the mapping if available, otherwise keep the original
    api_model = model_mapping.get(model, model)

    # Convert seed to int or None
    seed = int(seed) if seed != '-1' and seed.lstrip('-').isdigit() else None

    # Log generation request
    print(f"Generating images with: Model={model}, Format={format_enhance}, Style={style}")
    print(f"Advanced settings: Steps={steps}, Guidance Scale={guidance_scale}, Seed={seed}")
    print(f"Prompt: {prompt}")

    # Generate images
    result = leonardo_ai.generate_images(
        prompt=prompt,
        num_images=num_images,
        width=width,
        height=height,
        steps=steps,
        guidance_scale=guidance_scale,
        seed=seed,
        model=api_model  # Use the mapped model name
    )

    return jsonify(result)

@app.route('/apply_filter', methods=['POST'])
def apply_filter():
    # Get parameters from form
    session_id = request.form.get('session_id', '')
    image_id = int(request.form.get('image_id', 0))
    filter_type = request.form.get('filter_type', 'None')
    intensity = float(request.form.get('intensity', 0.5))

    # Apply filter
    result = leonardo_ai.apply_filter(session_id, image_id, filter_type, intensity)

    return jsonify(result)

@app.route('/download', methods=['GET'])
def download_image():
    session_id = request.args.get('session_id', '')
    image_id = int(request.args.get('image_id', 0))
    use_filtered = request.args.get('filtered', 'false').lower() == 'true'

    # Check if session and image exist
    if session_id not in leonardo_ai.generated_images or image_id >= len(leonardo_ai.generated_images[session_id]):
        return "Image not found", 404

    # Get the image path
    if use_filtered and 'filtered_path' in leonardo_ai.generated_images[session_id][image_id]:
        image_path = leonardo_ai.generated_images[session_id][image_id]['filtered_path']
    else:
        image_path = leonardo_ai.generated_images[session_id][image_id]['path']

    # Get format and quality
    format_str = request.args.get('format', 'png').lower()
    quality = int(request.args.get('quality', 95))

    # Open the image
    image = Image.open(image_path)

    # Convert to desired format
    output = io.BytesIO()
    if format_str == 'jpeg':
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(output, format='JPEG', quality=quality)
    elif format_str == 'png':
        image.save(output, format='PNG')
    elif format_str == 'gif':
        image.save(output, format='GIF')
    else:
        image.save(output, format='PNG')

    output.seek(0)

    # Generate filename
    filename = f"leonardo_ai_image.{format_str}"

    return send_file(
        output,
        mimetype=f'image/{format_str}',
        as_attachment=True,
        download_name=filename
    )

@app.route('/token_balance', methods=['GET'])
def get_token_balance():
    """Get the current token balance."""
    return jsonify({
        'success': True,
        'token_balance': leonardo_ai.get_token_balance()
    })

if __name__ == '__main__':
    # Use host 0.0.0.0 to make the server accessible from other devices on the network
    # Use port 5000 to avoid conflicts with other services
    port = 5000
    print(f"Starting server on http://localhost:{port}")
    try:
        app.run(debug=True, host='0.0.0.0', port=port)
    except OSError as e:
        # If the port is in use, try another port
        if "Address already in use" in str(e):
            port = 5001
            print(f"Port 5000 is in use. Trying port {port}...")
            app.run(debug=True, host='0.0.0.0', port=port)
        else:
            raise
