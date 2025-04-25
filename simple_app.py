import os
import sys
import torch
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import time
import io

class ImageGenerator:
    def __init__(self):
        """
        Initialize the ImageGenerator class.
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
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
            # For demonstration, create placeholder images
            return [self._create_placeholder_image(width, height) for _ in range(num_images)]
                
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

class LeonardoAIClone(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.image_generator = ImageGenerator()
        self.image_filter = ImageFilter()
        
        # Initialize state
        self.generated_images = []
        self.current_image = None
        self.filtered_image = None
        
        # Configure the window
        self.title("Leonardo AI Clone")
        self.geometry("1200x800")
        self.configure(bg="#1E1E1E")
        
        # Create the UI
        self.create_ui()
    
    def create_ui(self):
        # Configure style for dark theme
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#1E1E1E")
        self.style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF")
        self.style.configure("TButton", background="#4D4D4D", foreground="#FFFFFF")
        self.style.configure("TEntry", fieldbackground="#3D3D3D", foreground="#FFFFFF")
        
        # Main layout
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel (settings)
        self.left_frame = ttk.Frame(self.main_frame, width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Right panel (content)
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create settings panel
        self.create_settings_panel()
        
        # Create content panel
        self.create_content_panel()
    
    def create_settings_panel(self):
        # Settings header
        ttk.Label(self.left_frame, text="Settings", font=("Arial", 16, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Mode selection
        ttk.Label(self.left_frame, text="Mode").pack(anchor=tk.W, pady=(10, 5))
        self.mode_var = tk.StringVar(value="Creation")
        ttk.Radiobutton(self.left_frame, text="Creation", variable=self.mode_var, value="Creation").pack(anchor=tk.W)
        ttk.Radiobutton(self.left_frame, text="Legacy Mode", variable=self.mode_var, value="Legacy Mode").pack(anchor=tk.W)
        
        # Model selection
        ttk.Label(self.left_frame, text="Model").pack(anchor=tk.W, pady=(10, 5))
        self.model_var = tk.StringVar(value="FLUX 1.1")
        ttk.Combobox(self.left_frame, textvariable=self.model_var, values=["FLUX 1.1", "FLUX Ear", "Realistic", "Abstract", "Cartoon"]).pack(anchor=tk.W, fill=tk.X)
        
        # Number of images
        ttk.Label(self.left_frame, text="Number of Images").pack(anchor=tk.W, pady=(10, 5))
        self.num_images_var = tk.IntVar(value=1)
        ttk.Scale(self.left_frame, from_=1, to=4, variable=self.num_images_var, orient=tk.HORIZONTAL).pack(anchor=tk.W, fill=tk.X)
        
        # Advanced settings frame
        advanced_frame = ttk.LabelFrame(self.left_frame, text="Advanced Settings")
        advanced_frame.pack(anchor=tk.W, fill=tk.X, pady=(10, 5))
        
        # Width
        ttk.Label(advanced_frame, text="Width").pack(anchor=tk.W, pady=(5, 0))
        self.width_var = tk.IntVar(value=768)
        ttk.Scale(advanced_frame, from_=512, to=1024, variable=self.width_var, orient=tk.HORIZONTAL).pack(anchor=tk.W, fill=tk.X)
        
        # Height
        ttk.Label(advanced_frame, text="Height").pack(anchor=tk.W, pady=(5, 0))
        self.height_var = tk.IntVar(value=768)
        ttk.Scale(advanced_frame, from_=512, to=1024, variable=self.height_var, orient=tk.HORIZONTAL).pack(anchor=tk.W, fill=tk.X)
        
        # Steps
        ttk.Label(advanced_frame, text="Steps").pack(anchor=tk.W, pady=(5, 0))
        self.steps_var = tk.IntVar(value=50)
        ttk.Scale(advanced_frame, from_=20, to=100, variable=self.steps_var, orient=tk.HORIZONTAL).pack(anchor=tk.W, fill=tk.X)
        
        # Guidance Scale
        ttk.Label(advanced_frame, text="Guidance Scale").pack(anchor=tk.W, pady=(5, 0))
        self.guidance_var = tk.DoubleVar(value=7.5)
        ttk.Scale(advanced_frame, from_=1.0, to=20.0, variable=self.guidance_var, orient=tk.HORIZONTAL).pack(anchor=tk.W, fill=tk.X)
        
        # Seed
        ttk.Label(advanced_frame, text="Seed (-1 for random)").pack(anchor=tk.W, pady=(5, 0))
        self.seed_var = tk.IntVar(value=-1)
        ttk.Entry(advanced_frame, textvariable=self.seed_var).pack(anchor=tk.W, fill=tk.X, pady=(0, 5))
        
        # Upgrade banner
        upgrade_frame = ttk.Frame(self.left_frame, style="Upgrade.TFrame")
        upgrade_frame.pack(anchor=tk.W, fill=tk.X, pady=(20, 5))
        self.style.configure("Upgrade.TFrame", background="#3D3D3D")
        
        ttk.Label(upgrade_frame, text="Upgrade for Priority Generation", font=("Arial", 12, "bold"), style="Upgrade.TLabel").pack(anchor=tk.W, padx=10, pady=(10, 5))
        self.style.configure("Upgrade.TLabel", background="#3D3D3D", foreground="#FFFFFF")
        
        ttk.Label(upgrade_frame, text="Get faster generation times and priority in the queue.", style="Upgrade.TLabel").pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        ttk.Button(upgrade_frame, text="Upgrade Now", style="Upgrade.TButton").pack(anchor=tk.CENTER, padx=10, pady=(0, 10), fill=tk.X)
        self.style.configure("Upgrade.TButton", background="#4CAF50", foreground="#FFFFFF")
    
    def create_content_panel(self):
        # Prompt input
        prompt_frame = ttk.Frame(self.right_frame)
        prompt_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(prompt_frame, text="Enter your prompt", font=("Arial", 14, "bold")).pack(anchor=tk.W)
        
        self.prompt_text = ScrolledText(prompt_frame, height=5, bg="#3D3D3D", fg="#FFFFFF")
        self.prompt_text.pack(fill=tk.X, pady=(5, 0))
        
        # Generate button
        generate_button = ttk.Button(prompt_frame, text="Generate Images", command=self.generate_images, style="Generate.TButton")
        generate_button.pack(anchor=tk.W, pady=(10, 0))
        self.style.configure("Generate.TButton", background="#4CAF50", foreground="#FFFFFF")
        
        # Image display area
        self.image_frame = ttk.Frame(self.right_frame)
        self.image_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initial message
        ttk.Label(self.image_frame, text="Generated images will appear here.", font=("Arial", 12)).pack(anchor=tk.CENTER, expand=True)
        
        # Tabs for editing
        self.tabs = ttk.Notebook(self.right_frame)
        self.tabs.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Filters tab
        self.filters_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.filters_tab, text="Filters")
        
        # Edit tab
        self.edit_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.edit_tab, text="Edit")
        
        # Export tab
        self.export_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.export_tab, text="Export")
        
        # Create filter controls
        self.create_filter_controls()
        
        # Create edit controls
        self.create_edit_controls()
        
        # Create export controls
        self.create_export_controls()
    
    def create_filter_controls(self):
        # Split into two columns
        left_frame = ttk.Frame(self.filters_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        right_frame = ttk.Frame(self.filters_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Filter selection
        ttk.Label(left_frame, text="Select Filter").pack(anchor=tk.W, pady=(10, 5))
        self.filter_var = tk.StringVar(value="None")
        ttk.Combobox(left_frame, textvariable=self.filter_var, values=["None", "Sepia", "Grayscale", "Blur", "Sharpen"]).pack(anchor=tk.W, fill=tk.X)
        
        # Intensity slider
        ttk.Label(left_frame, text="Intensity").pack(anchor=tk.W, pady=(10, 5))
        self.intensity_var = tk.DoubleVar(value=0.5)
        ttk.Scale(left_frame, from_=0.0, to=1.0, variable=self.intensity_var, orient=tk.HORIZONTAL).pack(anchor=tk.W, fill=tk.X)
        
        # Apply button
        ttk.Button(left_frame, text="Apply Filter", command=self.apply_filter).pack(anchor=tk.W, pady=(10, 0))
        
        # Image display
        self.filter_image_label = ttk.Label(right_frame)
        self.filter_image_label.pack(fill=tk.BOTH, expand=True)
    
    def create_edit_controls(self):
        # Placeholder for edit controls
        ttk.Label(self.edit_tab, text="Editing features will be implemented in a future version.").pack(anchor=tk.CENTER, expand=True)
    
    def create_export_controls(self):
        # Split into two columns
        left_frame = ttk.Frame(self.export_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        right_frame = ttk.Frame(self.export_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Export format
        ttk.Label(left_frame, text="Export Format").pack(anchor=tk.W, pady=(10, 5))
        self.format_var = tk.StringVar(value="JPEG")
        ttk.Combobox(left_frame, textvariable=self.format_var, values=["JPEG", "PNG", "GIF"]).pack(anchor=tk.W, fill=tk.X)
        
        # Quality slider
        ttk.Label(left_frame, text="Quality").pack(anchor=tk.W, pady=(10, 5))
        self.quality_var = tk.IntVar(value=95)
        ttk.Scale(left_frame, from_=1, to=100, variable=self.quality_var, orient=tk.HORIZONTAL).pack(anchor=tk.W, fill=tk.X)
        
        # Filename
        ttk.Label(left_frame, text="Filename").pack(anchor=tk.W, pady=(10, 5))
        self.filename_var = tk.StringVar(value="leonardo_ai_image")
        ttk.Entry(left_frame, textvariable=self.filename_var).pack(anchor=tk.W, fill=tk.X)
        
        # Export button
        ttk.Button(left_frame, text="Export Image", command=self.export_image).pack(anchor=tk.W, pady=(10, 0))
        
        # Image display
        self.export_image_label = ttk.Label(right_frame)
        self.export_image_label.pack(fill=tk.BOTH, expand=True)
    
    def generate_images(self):
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        
        if not prompt:
            messagebox.showerror("Error", "Please enter a prompt first.")
            return
        
        # Show loading message
        loading_label = ttk.Label(self.image_frame, text="Generating images...", font=("Arial", 12))
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        loading_label.pack(anchor=tk.CENTER, expand=True)
        self.update()
        
        # Generate images in a separate thread
        def generate():
            self.generated_images = self.image_generator.generate(
                prompt=prompt,
                num_images=self.num_images_var.get(),
                width=self.width_var.get(),
                height=self.height_var.get(),
                steps=self.steps_var.get(),
                guidance_scale=self.guidance_var.get(),
                seed=None if self.seed_var.get() == -1 else self.seed_var.get()
            )
            
            # Update UI in the main thread
            self.after(0, self.display_generated_images)
        
        threading.Thread(target=generate).start()
    
    def display_generated_images(self):
        # Clear the image frame
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        
        if not self.generated_images:
            ttk.Label(self.image_frame, text="No images were generated.", font=("Arial", 12)).pack(anchor=tk.CENTER, expand=True)
            return
        
        # Create a grid for images
        grid_frame = ttk.Frame(self.image_frame)
        grid_frame.pack(fill=tk.BOTH, expand=True)
        
        # Calculate grid dimensions
        num_images = len(self.generated_images)
        cols = min(2, num_images)
        rows = (num_images + cols - 1) // cols
        
        # Add images to the grid
        for i, img in enumerate(self.generated_images):
            row = i // cols
            col = i % cols
            
            # Create a frame for the image
            img_frame = ttk.Frame(grid_frame)
            img_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Resize image for display
            display_img = img.copy()
            display_img.thumbnail((300, 300))
            
            # Convert to PhotoImage
            photo = self.pil_to_photoimage(display_img)
            
            # Create image label
            img_label = ttk.Label(img_frame, image=photo)
            img_label.image = photo  # Keep a reference
            img_label.pack(pady=(0, 5))
            
            # Add select button
            ttk.Button(img_frame, text=f"Select Image {i+1}", 
                      command=lambda idx=i: self.select_image(idx)).pack()
        
        # Configure grid weights
        for i in range(rows):
            grid_frame.rowconfigure(i, weight=1)
        for i in range(cols):
            grid_frame.columnconfigure(i, weight=1)
        
        # Select the first image by default
        if self.generated_images:
            self.select_image(0)
    
    def select_image(self, index):
        if 0 <= index < len(self.generated_images):
            self.current_image = self.generated_images[index]
            self.filtered_image = None
            
            # Update filter tab
            self.update_filter_preview()
            
            # Update export tab
            self.update_export_preview()
    
    def apply_filter(self):
        if self.current_image is None:
            messagebox.showerror("Error", "No image selected.")
            return
        
        filter_type = self.filter_var.get()
        intensity = self.intensity_var.get()
        
        if filter_type == "None":
            self.filtered_image = None
        else:
            self.filtered_image = self.image_filter.apply_filter(
                self.current_image,
                filter_type,
                intensity
            )
        
        # Update the preview
        self.update_filter_preview()
        self.update_export_preview()
    
    def update_filter_preview(self):
        # Display the current or filtered image in the filter tab
        img_to_display = self.filtered_image if self.filtered_image is not None else self.current_image
        
        if img_to_display is not None:
            # Resize for display
            display_img = img_to_display.copy()
            display_img.thumbnail((400, 400))
            
            # Convert to PhotoImage
            photo = self.pil_to_photoimage(display_img)
            
            # Update label
            self.filter_image_label.configure(image=photo)
            self.filter_image_label.image = photo  # Keep a reference
    
    def update_export_preview(self):
        # Display the current, filtered, or edited image in the export tab
        img_to_display = self.filtered_image if self.filtered_image is not None else self.current_image
        
        if img_to_display is not None:
            # Resize for display
            display_img = img_to_display.copy()
            display_img.thumbnail((400, 400))
            
            # Convert to PhotoImage
            photo = self.pil_to_photoimage(display_img)
            
            # Update label
            self.export_image_label.configure(image=photo)
            self.export_image_label.image = photo  # Keep a reference
    
    def export_image(self):
        img_to_export = self.filtered_image if self.filtered_image is not None else self.current_image
        
        if img_to_export is None:
            messagebox.showerror("Error", "No image to export.")
            return
        
        # Get export settings
        format_str = self.format_var.get().lower()
        quality = self.quality_var.get()
        filename = self.filename_var.get()
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{format_str}",
            filetypes=[(f"{format_str.upper()} files", f"*.{format_str}")],
            initialfile=f"{filename}.{format_str}"
        )
        
        if not file_path:
            return  # User cancelled
        
        try:
            # Convert RGBA to RGB if saving as JPEG
            if format_str.lower() == "jpeg" and img_to_export.mode == "RGBA":
                img_to_export = img_to_export.convert("RGB")
            
            # Save the image
            if format_str.lower() == "jpeg":
                img_to_export.save(file_path, format=format_str.upper(), quality=quality)
            else:
                img_to_export.save(file_path, format=format_str.upper())
            
            messagebox.showinfo("Success", f"Image exported successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export image: {e}")
    
    def pil_to_photoimage(self, pil_image):
        """Convert PIL Image to PhotoImage"""
        return tk.PhotoImage(data=self.pil_to_data(pil_image))
    
    def pil_to_data(self, pil_image):
        """Convert PIL Image to data for PhotoImage"""
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")
        return buffer.getvalue()

if __name__ == "__main__":
    app = LeonardoAIClone()
    app.mainloop()
