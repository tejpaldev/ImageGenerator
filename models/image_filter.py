import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

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
            elif filter_type == "Vintage":
                return self.vintage_filter(image, intensity)
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
        # Convert to numpy array
        img_array = np.array(image)
        
        # Apply sepia matrix
        sepia_matrix = np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ])
        
        # Apply the sepia transformation
        sepia_array = np.dot(img_array[...,:3], sepia_matrix.T)
        
        # Clip values to valid range
        sepia_array = np.clip(sepia_array, 0, 255).astype(np.uint8)
        
        # Create sepia image
        sepia_image = Image.fromarray(sepia_array)
        
        # Blend with original based on intensity
        return Image.blend(image, sepia_image, intensity)
    
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
    
    def vintage_filter(self, image, intensity=0.5):
        """
        Apply a vintage filter to the image.
        
        Args:
            image (PIL.Image): Input image
            intensity (float): Intensity of the filter (0.0 to 1.0)
            
        Returns:
            PIL.Image: Filtered image
        """
        # Convert to sepia first
        sepia_image = self.sepia_filter(image, intensity)
        
        # Adjust contrast
        contrast_enhancer = ImageEnhance.Contrast(sepia_image)
        contrast_image = contrast_enhancer.enhance(0.8)
        
        # Adjust brightness
        brightness_enhancer = ImageEnhance.Brightness(contrast_image)
        brightness_image = brightness_enhancer.enhance(0.9)
        
        # Add vignette effect
        vignette = self._create_vignette(image.size, intensity)
        
        # Apply vignette
        result = Image.composite(brightness_image, Image.new('RGB', image.size, (0, 0, 0)), vignette)
        
        return result
    
    def _create_vignette(self, size, intensity=0.5):
        """
        Create a vignette mask.
        
        Args:
            size (tuple): Size of the image (width, height)
            intensity (float): Intensity of the vignette effect
            
        Returns:
            PIL.Image: Vignette mask
        """
        width, height = size
        
        # Create a radial gradient
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 2
        
        # Create a new image for the mask
        mask = Image.new('L', size, 255)
        pixels = mask.load()
        
        # Fill the mask with a radial gradient
        for y in range(height):
            for x in range(width):
                # Calculate distance from center
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                
                # Calculate mask value based on distance
                mask_value = 255 - int(255 * (distance / radius) ** 2 * intensity)
                mask_value = max(0, min(255, mask_value))
                
                pixels[x, y] = mask_value
        
        return mask
