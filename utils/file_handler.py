import os
import io
from PIL import Image
from datetime import datetime

class FileHandler:
    def __init__(self, output_dir="outputs"):
        """
        Initialize the FileHandler class.
        
        Args:
            output_dir (str): Directory to save output files
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def save_image(self, image, filename, format="jpeg", quality=95):
        """
        Save an image to disk.
        
        Args:
            image (PIL.Image): Image to save
            filename (str): Base filename (without extension)
            format (str): Image format (jpeg, png, gif)
            quality (int): Quality for JPEG compression (1-100)
            
        Returns:
            str: Path to the saved file, or None if failed
        """
        try:
            # Generate a unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            full_filename = f"{filename}_{timestamp}.{format}"
            file_path = os.path.join(self.output_dir, full_filename)
            
            # Convert RGBA to RGB if saving as JPEG
            if format.lower() == "jpeg" and image.mode == "RGBA":
                image = image.convert("RGB")
            
            # Save the image
            if format.lower() == "jpeg":
                image.save(file_path, format=format.upper(), quality=quality)
            elif format.lower() == "png":
                image.save(file_path, format=format.upper())
            elif format.lower() == "gif":
                image.save(file_path, format=format.upper())
            else:
                image.save(file_path)
            
            return file_path
        except Exception as e:
            print(f"Error saving image: {e}")
            return None
    
    def load_image(self, file_path):
        """
        Load an image from disk.
        
        Args:
            file_path (str): Path to the image file
            
        Returns:
            PIL.Image: Loaded image, or None if failed
        """
        try:
            if os.path.exists(file_path):
                return Image.open(file_path)
            return None
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def image_to_bytes(self, image, format="jpeg", quality=95):
        """
        Convert a PIL image to bytes for download.
        
        Args:
            image (PIL.Image): Image to convert
            format (str): Image format (jpeg, png, gif)
            quality (int): Quality for JPEG compression (1-100)
            
        Returns:
            bytes: Image as bytes, or None if failed
        """
        try:
            # Convert RGBA to RGB if saving as JPEG
            if format.lower() == "jpeg" and image.mode == "RGBA":
                image = image.convert("RGB")
            
            # Save to bytes buffer
            buffer = io.BytesIO()
            
            if format.lower() == "jpeg":
                image.save(buffer, format=format.upper(), quality=quality)
            elif format.lower() == "png":
                image.save(buffer, format=format.upper())
            elif format.lower() == "gif":
                image.save(buffer, format=format.upper())
            else:
                image.save(buffer, format=format.upper())
            
            return buffer.getvalue()
        except Exception as e:
            print(f"Error converting image to bytes: {e}")
            return None
