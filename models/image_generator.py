import os
import numpy as np
from PIL import Image
import base64
import io
from together import Together
import time
from utils.config import TOGETHER_API_KEY, TOGETHER_MODEL

class ImageGenerator:
    def __init__(self):
        """
        Initialize the ImageGenerator class.
        """
        pass

    def generate(self, prompt, num_images=1, width=1024, height=768, steps=4, guidance_scale=7.5, seed=None):
        """
        Generate images based on the provided prompt using the Together API.

        Args:
            prompt (str): Text prompt for image generation
            num_images (int): Number of images to generate
            width (int): Width of the generated images
            height (int): Height of the generated images
            steps (int): Number of denoising steps
            guidance_scale (float): Guidance scale for the model (not used by Together API)
            seed (int, optional): Random seed for reproducibility (not used by Together API)

        Returns:
            list: List of generated PIL images
        """
        try:
            if TOGETHER_API_KEY:
                return self._generate_with_together_api(
                    prompt=prompt,
                    num_images=num_images,
                    width=width,
                    height=height,
                    steps=steps
                )
            else:
                print("No Together API key found. Please set the TOGETHER_API_KEY environment variable.")
                # Return placeholder images if no API key is available
                return [self._create_placeholder_image(width, height) for _ in range(num_images)]

        except Exception as e:
            print(f"Error generating images: {e}")
            # Return placeholder images for demonstration
            return [self._create_placeholder_image(width, height) for _ in range(num_images)]

    def _generate_with_together_api(self, prompt, num_images=1, width=1024, height=768, steps=4):
        """
        Generate images using the Together API.

        Args:
            prompt (str): Text prompt for image generation
            num_images (int): Number of images to generate
            width (int): Width of the generated images
            height (int): Height of the generated images
            steps (int): Number of denoising steps

        Returns:
            list: List of generated PIL images
        """
        try:
            print(f"Generating images with Together API: {prompt}")

            # Initialize the Together client
            client = Together(api_key=TOGETHER_API_KEY)

            # Prepare the images list
            images = []

            # Generate the requested number of images
            for i in range(num_images):
                # Generate image with Together API
                response = client.images.generate(
                    prompt=prompt,
                    model=TOGETHER_MODEL,
                    width=width,
                    height=height,
                    steps=steps,
                    n=1,
                    response_format="b64_json",
                    stop=[]
                )

                # Decode and convert to PIL Image
                image_data = base64.b64decode(response.data[0].b64_json)
                image = Image.open(io.BytesIO(image_data))
                images.append(image)

                # Add a small delay between requests to avoid rate limiting
                if i < num_images - 1:
                    time.sleep(0.5)

            return images

        except Exception as e:
            print(f"Error generating images with Together API: {e}")
            # Return placeholder images as fallback
            return [self._create_placeholder_image(width, height) for _ in range(num_images)]

    def _create_placeholder_image(self, width, height):
        """
        Create a placeholder image for demonstration purposes.

        Args:
            width (int): Width of the image
            height (int): Height of the image

        Returns:
            PIL.Image: A placeholder image
        """
        # Create a gradient image as a placeholder
        array = np.zeros((height, width, 3), dtype=np.uint8)

        # Create a gradient effect
        for y in range(height):
            for x in range(width):
                r = int(255 * (x / width))
                g = int(255 * (y / height))
                b = int(255 * ((x + y) / (width + height)))
                array[y, x] = [r, g, b]

        return Image.fromarray(array)

    def save_image(self, image, image_path):
        """
        Save an image to disk.

        Args:
            image (PIL.Image): Image to save
            image_path (str): Path to save the image

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(image_path), exist_ok=True)

            # Save the image
            image.save(image_path)

            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
