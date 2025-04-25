import numpy as np
from PIL import Image, ImageEnhance, ImageOps
import cv2

class ImageEditor:
    def __init__(self):
        """
        Initialize the ImageEditor class.
        """
        pass
    
    def crop(self, image, left, top, right, bottom):
        """
        Crop the image based on percentage values.
        
        Args:
            image (PIL.Image): Input image
            left (int): Left crop percentage (0-100)
            top (int): Top crop percentage (0-100)
            right (int): Right crop percentage (0-100)
            bottom (int): Bottom crop percentage (0-100)
            
        Returns:
            PIL.Image: Cropped image
        """
        try:
            width, height = image.size
            
            # Convert percentages to pixel values
            left_px = int(width * left / 100)
            top_px = int(height * top / 100)
            right_px = int(width * right / 100)
            bottom_px = int(height * bottom / 100)
            
            # Ensure valid crop box
            if left_px >= right_px or top_px >= bottom_px:
                return image
            
            # Crop the image
            cropped_image = image.crop((left_px, top_px, right_px, bottom_px))
            
            return cropped_image
        except Exception as e:
            print(f"Error cropping image: {e}")
            return image
    
    def rotate(self, image, angle):
        """
        Rotate the image by the specified angle.
        
        Args:
            image (PIL.Image): Input image
            angle (float): Rotation angle in degrees
            
        Returns:
            PIL.Image: Rotated image
        """
        try:
            # Rotate the image
            rotated_image = image.rotate(angle, expand=True, resample=Image.BICUBIC)
            
            return rotated_image
        except Exception as e:
            print(f"Error rotating image: {e}")
            return image
    
    def resize(self, image, width, height):
        """
        Resize the image to the specified dimensions.
        
        Args:
            image (PIL.Image): Input image
            width (int): Target width
            height (int): Target height
            
        Returns:
            PIL.Image: Resized image
        """
        try:
            # Resize the image
            resized_image = image.resize((width, height), Image.LANCZOS)
            
            return resized_image
        except Exception as e:
            print(f"Error resizing image: {e}")
            return image
    
    def adjust_colors(self, image, brightness=1.0, contrast=1.0, saturation=1.0):
        """
        Adjust color properties of the image.
        
        Args:
            image (PIL.Image): Input image
            brightness (float): Brightness adjustment factor
            contrast (float): Contrast adjustment factor
            saturation (float): Saturation adjustment factor
            
        Returns:
            PIL.Image: Color-adjusted image
        """
        try:
            # Adjust brightness
            brightness_enhancer = ImageEnhance.Brightness(image)
            img = brightness_enhancer.enhance(brightness)
            
            # Adjust contrast
            contrast_enhancer = ImageEnhance.Contrast(img)
            img = contrast_enhancer.enhance(contrast)
            
            # Adjust saturation
            saturation_enhancer = ImageEnhance.Color(img)
            img = saturation_enhancer.enhance(saturation)
            
            return img
        except Exception as e:
            print(f"Error adjusting colors: {e}")
            return image
    
    def remove_background(self, image):
        """
        Remove the background from the image.
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            PIL.Image: Image with background removed
        """
        try:
            # Convert PIL image to OpenCV format
            img_cv = np.array(image)
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
            
            # Create a simple mask using GrabCut algorithm
            mask = np.zeros(img_cv.shape[:2], np.uint8)
            bgd_model = np.zeros((1, 65), np.float64)
            fgd_model = np.zeros((1, 65), np.float64)
            
            # Define rectangle for initial segmentation
            height, width = img_cv.shape[:2]
            rect = (width//10, height//10, width*8//10, height*8//10)
            
            # Apply GrabCut
            cv2.grabCut(img_cv, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
            
            # Create mask where sure and probable foreground are set to 1, else 0
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            
            # Multiply image with the mask to keep foreground only
            img_cv = img_cv * mask2[:, :, np.newaxis]
            
            # Convert back to PIL
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            result = Image.fromarray(img_cv)
            
            # Create a transparent background
            result = result.convert("RGBA")
            data = result.getdata()
            
            new_data = []
            for item in data:
                # Change all black (or near black) pixels to transparent
                if item[0] < 5 and item[1] < 5 and item[2] < 5:
                    new_data.append((0, 0, 0, 0))
                else:
                    new_data.append(item)
            
            result.putdata(new_data)
            
            return result
        except Exception as e:
            print(f"Error removing background: {e}")
            return image
