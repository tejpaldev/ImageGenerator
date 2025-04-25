import os
import torch
import numpy as np
from PIL import Image
from diffusers import DiffusionPipeline, FluxPipeline
from transformers import set_seed
import time

class ImageGenerator:
    def __init__(self):
        """
        Initialize the ImageGenerator class.
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.model_name = None
        
    def load_model(self, model_name="FLUX 1.1"):
        """
        Load the specified model.
        
        Args:
            model_name (str): Name of the model to load
            
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            # Only load if model not already loaded or if different model requested
            if self.model is None or self.model_name != model_name:
                if model_name == "FLUX 1.1":
                    # Load FLUX 1.1 model
                    self.model = FluxPipeline.from_pretrained(
                        "black-forest-labs/FLUX.1-schnell", 
                        torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                    )
                    
                    # Enable CPU offload if using GPU to save VRAM
                    if self.device == "cuda":
                        self.model.enable_model_cpu_offload()
                    
                    self.model_name = model_name
                    return True
                else:
                    # For other models, we'll use a fallback to Stable Diffusion
                    self.model = DiffusionPipeline.from_pretrained(
                        "runwayml/stable-diffusion-v1-5",
                        torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                    )
                    
                    # Enable CPU offload if using GPU to save VRAM
                    if self.device == "cuda":
                        self.model.enable_model_cpu_offload()
                    
                    self.model_name = model_name
                    return True
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def generate(self, prompt, num_images=1, width=768, height=768, steps=50, guidance_scale=7.5, seed=None):
        """
        Generate images based on the provided prompt.
        
        Args:
            prompt (str): Text prompt for image generation
            num_images (int): Number of images to generate
            width (int): Width of the generated images
            height (int): Height of the generated images
            steps (int): Number of denoising steps
            guidance_scale (float): Guidance scale for the model
            seed (int, optional): Random seed for reproducibility
            
        Returns:
            list: List of generated PIL images
        """
        try:
            # Load the model if not already loaded
            if not self.load_model():
                return []
            
            # Set seed for reproducibility if provided
            if seed is not None:
                set_seed(seed)
                generator = torch.Generator(device="cpu").manual_seed(seed)
            else:
                generator = None
            
            # Generate images
            if self.model_name == "FLUX 1.1":
                # FLUX model uses fewer steps
                actual_steps = min(steps, 4)
                
                result = self.model(
                    prompt=prompt,
                    num_inference_steps=actual_steps,
                    guidance_scale=guidance_scale,
                    width=width,
                    height=height,
                    num_images_per_prompt=num_images,
                    generator=generator,
                    output_type="pil"
                )
                
                return result.images
            else:
                # For other models (Stable Diffusion fallback)
                result = self.model(
                    prompt=prompt,
                    num_inference_steps=steps,
                    guidance_scale=guidance_scale,
                    width=width,
                    height=height,
                    num_images_per_prompt=num_images,
                    generator=generator,
                    output_type="pil"
                )
                
                return result.images
                
        except Exception as e:
            print(f"Error generating images: {e}")
            # Return placeholder images for demonstration
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
