import requests
import os
from pathlib import Path

def test_api():
    """Test the Wav2Lip API with sample files"""
    
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    print("Testing health endpoint...")
    response = requests.get(f"{base_url}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    
    # Test video generation (you'll need to provide actual image and audio files)
    image_path = "test_image.jpg"  # Replace with actual image path
    audio_path = "test_audio.wav"  # Replace with actual audio path
    
    if os.path.exists(image_path) and os.path.exists(audio_path):
        print(f"\nTesting video generation with {image_path} and {audio_path}...")
        
        with open(image_path, 'rb') as img, open(audio_path, 'rb') as aud:
            files = {
                'image': ('image.jpg', img, 'image/jpeg'),
                'audio': ('audio.wav', aud, 'audio/wav')
            }
            data = {
                'fps': 25,
                'static': True,
                'wav2lip_batch_size': 64,  # Smaller batch size for testing
                'resize_factor': 1
            }
            
            try:
                response = requests.post(f"{base_url}/generate-video", 
                                       files=files, data=data, timeout=300)
                
                if response.status_code == 200:
                    output_path = "test_output.mp4"
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Success! Video saved as {output_path}")
                    print(f"File size: {len(response.content)} bytes")
                else:
                    print(f"Error {response.status_code}: {response.text}")
                    
            except requests.exceptions.Timeout:
                print("Request timed out - video generation may take longer")
            except Exception as e:
                print(f"Error: {e}")
    else:
        print(f"\nSkipping video generation test - missing files:")
        print(f"  Image: {image_path} (exists: {os.path.exists(image_path)})")
        print(f"  Audio: {audio_path} (exists: {os.path.exists(audio_path)})")

if __name__ == "__main__":
    test_api()
