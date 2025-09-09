# Wav2Lip REST API

A FastAPI-based REST API for generating lip-sync videos using the Wav2Lip model.

## Features

- **REST API**: Simple HTTP endpoints for video generation
- **File Upload**: Support for various image and audio formats
- **Configurable**: Adjustable parameters for quality and performance
- **GPU Support**: Automatic GPU detection and usage
- **Error Handling**: Comprehensive error handling and validation

## Requirements

- Python 3.8+
- FFmpeg (for audio/video processing)
- CUDA (optional, for GPU acceleration)
- Wav2Lip model checkpoint

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download the Wav2Lip model checkpoint and place it in the appropriate directory.

3. Ensure FFmpeg is installed and available in your system PATH.

## Usage

### Start the API Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

### API Endpoints

#### 1. Health Check
```
GET /health
```
Returns the API status and configuration.

#### 2. Generate Video (Synchronous)
```
POST /generate-video
```

**Parameters:**
- `image` (file): Image file (JPG, PNG, JPEG)
- `audio` (file): Audio file (WAV, MP3, etc.)
- `fps` (float, optional): Frames per second (default: 25.0)
- `resize_factor` (int, optional): Resolution reduction factor (default: 1)
- `wav2lip_batch_size` (int, optional): Batch size (default: 128)
- `img_size` (int, optional): Face image size (default: 96)
- `static` (bool, optional): Use only first frame (default: true)

**Response:**
Returns an MP4 video file with lip-sync animation.

#### 3. Generate Video (Asynchronous)
```
POST /generate-video-async
```
Same parameters as above, but returns a job ID for tracking.

#### 4. Check Job Status
```
GET /job-status/{job_id}
```
Returns the status of an asynchronous job.

### Example Usage with curl

```bash
# Generate video
curl -X POST "http://localhost:8000/generate-video" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@path/to/image.jpg" \
  -F "audio=@path/to/audio.wav" \
  -F "fps=25" \
  --output result.mp4

# Check health
curl "http://localhost:8000/health"
```

### Example Usage with Python

```python
import requests

# Upload files and generate video
with open('image.jpg', 'rb') as img, open('audio.wav', 'rb') as aud:
    files = {
        'image': img,
        'audio': aud
    }
    data = {
        'fps': 25,
        'static': True
    }
    
    response = requests.post('http://localhost:8000/generate-video', 
                           files=files, data=data)
    
    if response.status_code == 200:
        with open('output.mp4', 'wb') as f:
            f.write(response.content)
        print("Video generated successfully!")
    else:
        print(f"Error: {response.status_code}")
```

## Configuration

### Model Checkpoint

Update the `DEFAULT_CHECKPOINT_PATH` in `main.py` to point to your Wav2Lip model checkpoint:

```python
DEFAULT_CHECKPOINT_PATH = "path/to/your/wav2lip_gan.pth"
```

### Performance Tuning

- **GPU Usage**: The API automatically detects and uses GPU if available
- **Batch Size**: Adjust `wav2lip_batch_size` for memory optimization
- **Image Size**: Smaller `img_size` values process faster but may reduce quality
- **Resolution**: Use `resize_factor` > 1 to reduce input resolution

## API Documentation

Once the server is running, visit:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Error Handling

The API includes comprehensive error handling for:
- Invalid file formats
- Missing model checkpoints
- Face detection failures
- Processing errors
- File I/O issues

## Limitations

- Face must be clearly visible in the input image/video
- Audio quality affects lip-sync accuracy
- Processing time depends on video length and hardware
- GPU memory limits batch sizes for high-resolution inputs

## Troubleshooting

### Common Issues

1. **"Face not detected" error**: Ensure the input image contains a clear, front-facing face
2. **"Model checkpoint not found"**: Verify the checkpoint path and file exists
3. **Out of memory errors**: Reduce batch size or image resolution
4. **FFmpeg errors**: Ensure FFmpeg is properly installed and in PATH

### Performance Tips

- Use GPU for faster processing
- Reduce `resize_factor` for faster processing of high-resolution inputs
- Adjust `wav2lip_batch_size` based on available memory
- Use static images (single frame) for faster processing when possible
