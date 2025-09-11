import os
import sys
import tempfile
import shutil
from pathlib import Path
import uuid
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Body
from fastapi.responses import FileResponse
import uvicorn
import torch

from wav2lip import run
from model.config_model import Wav2LipConfig

app = FastAPI(
    title="Wav2Lip API",
    description="REST API for generating lip-sync videos using Wav2Lip",
    version="1.0.0"
)

# Global settings
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using {device} for inference.')

@app.get("/")
async def root():
    return {"message": "Wav2Lip API", "status": "running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

@app.get("/config/schema")
async def get_config_schema():
    """Get the JSON schema for the Wav2Lip configuration."""
    return Wav2LipConfig.schema()

@app.get("/config/default")
async def get_default_config():
    """Get the default Wav2Lip configuration."""
    return Wav2LipConfig().dict()

@app.post("/config/validate")
async def validate_config(config: Wav2LipConfig):
    """Validate a Wav2Lip configuration."""
    return {
        "valid": True,
        "config": config.dict(),
        "quality_description": config.get_quality_description(),
        "resolution_scale": config.get_resolution_scale(),
        "is_custom_resolution": config.is_custom_resolution()
    }

@app.post("/generate-video")
async def generate_video(
    image: UploadFile = File(..., description="Image file (JPG, PNG, JPEG)"),
    audio: UploadFile = File(..., description="Audio file (WAV, MP3, etc.)"),
    config: Optional[Wav2LipConfig] = Body(None, description="Wav2Lip configuration settings")
):
    """
    Generate a lip-sync video from an image and audio file.
    
    Args:
        image: Image file (JPG, PNG, JPEG)
        audio: Audio file (WAV, MP3, etc.)
        config: Optional Wav2Lip configuration as JSON
    
    Returns an MP4 video file with the generated lip-sync animation.
    """
    
    # Use default config if none provided
    if config is None:
        config = Wav2LipConfig()
    
    # Validate file types
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Image must be an image file")
    
    if not audio.content_type.startswith('audio/') and not audio.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="Audio must be an audio or video file")
    
    # Create temporary directory for processing
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Save uploaded files
        image_path = os.path.join(temp_dir, f"input_image{Path(image.filename).suffix}")
        audio_path = os.path.join(temp_dir, f"input_audio{Path(audio.filename).suffix}")
        output_path = os.path.join(temp_dir, f"output_{uuid.uuid4()}.mp4")
        
        # Save image
        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)
        
        # Save audio  
        with open(audio_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)
        
        # Process the video with configuration
        run(
            video_path=image_path,
            audio_path=audio_path,
            output_path=output_path,
            config=config  # Pass the configuration
        )
        
        # Check if output file was created
        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="Failed to generate video")
        
        # Create response filename with quality info
        filename = f"lip_sync_video_{config.OPTIONS.quality.lower()}_{uuid.uuid4()}.mp4"
        
        # Return the generated video
        return FileResponse(
            output_path,
            media_type="video/mp4",
            filename=filename,
            background=None  # Keep file until response is sent
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")
    
    finally:
        # Clean up temporary directory (except the output file which is handled by FastAPI)
        try:
            for file in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file)
                if file_path != output_path:  # Don't delete the output file yet
                    try:
                        os.remove(file_path)
                    except:
                        pass
        except:
            pass

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
