# Wav2Lip API Startup Script

Write-Host "Starting Wav2Lip API..." -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>$null
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found. Please install Python 3.8 or later." -ForegroundColor Red
    exit 1
}

# Check if FFmpeg is available
try {
    $ffmpegVersion = ffmpeg -version 2>$null | Select-String "ffmpeg version" | Select-Object -First 1
    Write-Host "Found FFmpeg: $($ffmpegVersion.Line)" -ForegroundColor Green
} catch {
    Write-Host "Warning: FFmpeg not found. Please install FFmpeg for audio/video processing." -ForegroundColor Yellow
    Write-Host "You can download FFmpeg from: https://ffmpeg.org/download.html" -ForegroundColor Yellow
}

# Check if virtual environment exists
if (Test-Path "venv") {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & .\venv\Scripts\Activate.ps1
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    python -m venv venv
    & .\venv\Scripts\Activate.ps1
}

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Green
pip install -r requirements.txt

# Check for model checkpoint
$checkpointPath = "..\Wav2Lip\checkpoints\wav2lip_gan.pth"
if (Test-Path $checkpointPath) {
    Write-Host "Found model checkpoint at: $checkpointPath" -ForegroundColor Green
} else {
    Write-Host "Warning: Model checkpoint not found at: $checkpointPath" -ForegroundColor Yellow
    Write-Host "Please download the Wav2Lip model checkpoint and place it in the checkpoints directory." -ForegroundColor Yellow
    Write-Host "You can download it from: https://github.com/Rudrabha/Wav2Lip" -ForegroundColor Yellow
}

# Start the API server
Write-Host "Starting FastAPI server..." -ForegroundColor Green
Write-Host "API will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API documentation at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow

python main.py
