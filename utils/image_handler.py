"""
Image Handler - Cultural Chronicles

This module handles image upload, processing, optimization, and storage
for cultural heritage images submitted with stories.
"""

import os
import uuid
import logging
from PIL import Image
import streamlit as st
from io import BytesIO

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
UPLOAD_DIR = "uploads"
MAX_IMAGE_SIZE = (1200, 1200)  # Maximum dimensions
QUALITY = 85  # JPEG quality
ALLOWED_FORMATS = ['PNG', 'JPEG', 'JPG', 'GIF', 'BMP', 'WEBP']

def ensure_upload_directory():
    """Ensure the upload directory exists"""
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        logger.info(f"Upload directory ensured: {UPLOAD_DIR}")
    except Exception as e:
        logger.error(f"Failed to create upload directory: {str(e)}")
        raise

def validate_image(uploaded_file):
    """
    Validate uploaded image file
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    try:
        # Check file size (5MB limit)
        if uploaded_file.size > 5 * 1024 * 1024:
            return False, "Image size must be less than 5MB"
        
        # Check file type
        if uploaded_file.type not in ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/bmp', 'image/webp']:
            return False, "Invalid image format. Supported formats: PNG, JPEG, JPG, GIF, BMP, WEBP"
        
        # Try to open the image to verify it's valid
        Image.open(uploaded_file).verify()
        
        return True, ""
        
    except Exception as e:
        logger.error(f"Image validation failed: {str(e)}")
        return False, f"Invalid image file: {str(e)}"

def optimize_image(image, format='JPEG'):
    """
    Optimize image by resizing and compressing
    
    Args:
        image: PIL Image object
        format: Output format
        
    Returns:
        BytesIO: Optimized image data
    """
    try:
        # Convert RGBA to RGB for JPEG
        if format == 'JPEG' and image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        
        # Resize if too large
        if image.size[0] > MAX_IMAGE_SIZE[0] or image.size[1] > MAX_IMAGE_SIZE[1]:
            image.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
            logger.info(f"Image resized to: {image.size}")
        
        # Save optimized image to BytesIO
        output = BytesIO()
        save_kwargs = {'format': format}
        
        if format == 'JPEG':
            save_kwargs['quality'] = QUALITY
            save_kwargs['optimize'] = True
        elif format == 'PNG':
            save_kwargs['optimize'] = True
        
        image.save(output, **save_kwargs)
        output.seek(0)
        
        return output
        
    except Exception as e:
        logger.error(f"Image optimization failed: {str(e)}")
        raise

def generate_unique_filename(original_filename):
    """
    Generate a unique filename for the uploaded image
    
    Args:
        original_filename: Original filename from upload
        
    Returns:
        str: Unique filename
    """
    try:
        # Get file extension
        file_ext = os.path.splitext(original_filename)[1].lower()
        if not file_ext:
            file_ext = '.jpg'  # Default extension
        
        # Generate unique filename using UUID
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        
        return unique_filename
        
    except Exception as e:
        logger.error(f"Filename generation failed: {str(e)}")
        return f"{uuid.uuid4().hex}.jpg"

def handle_image_upload(uploaded_file):
    """
    Handle complete image upload process: validation, optimization, and storage
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        str or None: Path to saved image file, None if failed
    """
    try:
        # Ensure upload directory exists
        ensure_upload_directory()
        
        # Validate image
        is_valid, error_message = validate_image(uploaded_file)
        if not is_valid:
            st.error(f"❌ Image validation failed: {error_message}")
            return None
        
        # Reset file pointer
        uploaded_file.seek(0)
        
        # Open and process image
        image = Image.open(uploaded_file)
        logger.info(f"Processing image: {uploaded_file.name}, size: {image.size}, mode: {image.mode}")
        
        # Determine output format
        original_format = image.format
        if original_format in ['JPEG', 'JPG']:
            output_format = 'JPEG'
            file_extension = '.jpg'
        elif original_format == 'PNG':
            output_format = 'PNG'
            file_extension = '.png'
        else:
            # Convert other formats to JPEG
            output_format = 'JPEG'
            file_extension = '.jpg'
        
        # Optimize image
        optimized_image_data = optimize_image(image, output_format)
        
        # Generate unique filename
        unique_filename = generate_unique_filename(uploaded_file.name)
        # Ensure correct extension
        unique_filename = os.path.splitext(unique_filename)[0] + file_extension
        
        # Save file
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, 'wb') as f:
            f.write(optimized_image_data.getvalue())
        
        logger.info(f"Image saved successfully: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Image upload failed: {str(e)}")
        st.error(f"❌ Image upload failed: {str(e)}")
        return None

def get_image_info(file_path):
    """
    Get information about a saved image
    
    Args:
        file_path: Path to the image file
        
    Returns:
        dict: Image information
    """
    try:
        if not os.path.exists(file_path):
            return None
        
        with Image.open(file_path) as img:
            return {
                'size': img.size,
                'format': img.format,
                'mode': img.mode,
                'file_size': os.path.getsize(file_path)
            }
            
    except Exception as e:
        logger.error(f"Failed to get image info: {str(e)}")
        return None

def delete_image(file_path):
    """
    Delete an image file
    
    Args:
        file_path: Path to the image file
        
    Returns:
        bool: True if deleted successfully, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Image deleted: {file_path}")
            return True
        else:
            logger.warning(f"Image not found for deletion: {file_path}")
            return False
            
    except Exception as e:
        logger.error(f"Failed to delete image: {str(e)}")
        return False

def cleanup_orphaned_images():
    """
    Clean up orphaned image files (images not referenced in database)
    This function should be called periodically to maintain storage efficiency
    """
    try:
        # This would require database integration to check which images are referenced
        # For now, just log the intent
        logger.info("Orphaned image cleanup would be performed here")
        
    except Exception as e:
        logger.error(f"Image cleanup failed: {str(e)}")
