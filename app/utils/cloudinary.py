import os
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
from typing import Optional

def init_cloudinary():
    """Initialize Cloudinary with credentials from environment variables"""
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )

async def upload_media(file: UploadFile, folder: str = "stories") -> Optional[str]:
    """
    Upload media file to Cloudinary
    Returns the URL of the uploaded file or None if upload fails
    """
    try:
        # Read file content
        contents = await file.read()
        
        # Upload to cloudinary
        result = cloudinary.uploader.upload(
            contents,
            folder=folder,
            resource_type="auto",  # Automatically detect if it's image or video
        )
        
        # Return the secure URL
        return result["secure_url"]
    except Exception as e:
        print(f"Error uploading to Cloudinary: {str(e)}")
        return None
    finally:
        await file.seek(0)  # Reset file pointer 